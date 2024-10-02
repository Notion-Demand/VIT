from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load your dataset
data = pd.read_csv('Orders_New_query_2024_07_01.csv')

def recommend_items_with_similarity(area, item, data, n_recommendations=5):
    data['billing_address_state'] = data['billing_address_state'].str.strip().str.upper()
    area_item_matrix = data.pivot_table(index='billing_address_state', columns='sku_id', values='ordered_quantity', aggfunc='sum').fillna(0)
    item_similarity_matrix = pd.DataFrame(cosine_similarity(area_item_matrix.T), index=area_item_matrix.columns, columns=area_item_matrix.columns)
    area = area.strip().upper()

    if area not in area_item_matrix.index:
        return None

    items_in_area = area_item_matrix.loc[area].sort_values(ascending=False)

    if item not in items_in_area or items_in_area[item] == 0:
        return items_in_area.head(n_recommendations)

    recommendations = items_in_area[items_in_area.index != item].head(n_recommendations)
    similarity_scores = item_similarity_matrix.loc[item, recommendations.index]

    recommendations_with_similarity = pd.DataFrame({
        'SKU ID': recommendations.index,
        'Ordered Quantity': recommendations.values,
        'Gross Merchandise Value': data.groupby('sku_id')['gross_merchandise_value'].sum().reindex(recommendations.index, fill_value=0).values,
    }).sort_values(by='Ordered Quantity', ascending=False)

    return recommendations_with_similarity[['SKU ID', 'Ordered Quantity', 'Gross Merchandise Value']]

def get_recommendations(sku_id, data, top_n=20):
    data.fillna(0, inplace=True)
    scaler = MinMaxScaler()
    numerical_features = ['gross_merchandise_value', 'net_sales_before_tax', 'gift_wrap_expense', 'packaging_expense', 'handling_expense', 'shipping_expense']

    for col in numerical_features:
        data[col] = pd.to_numeric(data[col], errors='coerce')

    data.dropna(subset=numerical_features, inplace=True)
    data[numerical_features] = scaler.fit_transform(data[numerical_features])
    categorical_features = ['source', 'refund_status', 'rto_status', 'cancellation_status', 'order_status', 'payment_status', 'billing_address_state']
    data = pd.get_dummies(data, columns=categorical_features)

    product_profiles = data.groupby('sku_id')[numerical_features].mean().reset_index()
    feature_matrix = product_profiles.drop('sku_id', axis=1)
    similarity_matrix = cosine_similarity(feature_matrix)

    sku_id_to_index = {sku_id: index for index, sku_id in enumerate(product_profiles['sku_id'])}

    if sku_id not in sku_id_to_index:
        return pd.DataFrame(columns=['SKU ID', 'Ordered Quantity', 'Gross Merchandise Value'])

    index = sku_id_to_index[sku_id]
    similarity_scores = list(enumerate(similarity_matrix[index]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    top_sku_indices = [i for i, score in similarity_scores[1:top_n + 1]]
    recommended_skus = product_profiles.iloc[top_sku_indices]['sku_id'].tolist()

    ordered_quantity = data.groupby('sku_id')['ordered_quantity'].sum().reindex(recommended_skus, fill_value=0).tolist()
    gmv = data.groupby('sku_id')['gross_merchandise_value'].sum().reindex(recommended_skus, fill_value=0).tolist()

    recommendation_df = pd.DataFrame({
        'SKU ID': recommended_skus,
        'Ordered Quantity': ordered_quantity,
        'Gross Merchandise Value': gmv,
    })
    return recommendation_df[['SKU ID', 'Ordered Quantity', 'Gross Merchandise Value']]

def analyze_orders(data):
    data['order_date_time_utc'] = pd.to_datetime(data['order_date_time_utc'], errors='coerce')
    filtered_data = data[(data['order_date_time_utc'].dt.month.isin([2, 3])) & (data['order_date_time_utc'].dt.year == 2024)]
    filtered_data = filtered_data[filtered_data['sku_id'] != 0]

    sku_summary = filtered_data.groupby('sku_id').agg({
        'ordered_quantity': 'sum',
        'gross_merchandise_value': 'sum',
        'cancellation_status': lambda x: (x == 'TRUE').sum()
    }).reset_index()

    most_ordered = sku_summary.sort_values(by=['ordered_quantity'], ascending=False).head(10)
    least_ordered = sku_summary.sort_values(by=['ordered_quantity'], ascending=True).head(10)

    most_ordered_display = most_ordered[['sku_id', 'ordered_quantity', 'gross_merchandise_value']]
    least_ordered_display = least_ordered[['sku_id', 'ordered_quantity', 'gross_merchandise_value']]

    return most_ordered_display, least_ordered_display

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    area = request.form['area']
    sku_id = request.form['sku_id']
    method = request.form['method']

    if method == 'area_popularity':
        recommendations = recommend_items_with_similarity(area, sku_id, data)
    else:
        recommendations = get_recommendations(sku_id, data)

    most_ordered, least_ordered = analyze_orders(data)
    
    return jsonify({
        'recommendations': recommendations.to_dict(orient='records') if recommendations is not None else [],
        'most_ordered': most_ordered.to_dict(orient='records'),
        'least_ordered': least_ordered.to_dict(orient='records')
    })

if __name__ == '__main__':
    app.run(debug=True)

