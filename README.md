# Heart Disease Detection

## 1. Executive Summary
This project aims to predict the presence of heart disease in patients using a clinical dataset. A Logistic Regression model was developed, achieving an accuracy of approximately **82.4%** and a ROC AUC score of **0.88**.

## 2. Data Overview & Preprocessing
- **Dataset**: The 'heart.csv' file contains 1,025 records with 14 original features.
- **Data Cleaning**: No missing values were detected. Features were renamed for better readability (e.g., `cp` to `Chest_Pain_Type`).
- **Feature Selection**: Based on importance, 10 key features were selected: `Thalassemia`, `Chest_Pain_Type`, `Major_Vessels`, `ST_Depression`, `Exercise_Induced_Angina`, `Max_Heart_Rate`, `ST_Slope`, `Age`, `Sex`, and `Resting_ECG`.
- **Scaling**: Data was standardized using `StandardScaler` to ensure all features contribute equally to the model.

## 3. Modeling: Logistic Regression
Logistic Regression was chosen as the primary classifier. It uses the sigmoid function to map linear combinations of inputs into probabilities.
- **Training Split**: 80% Train / 20% Test.
- **Hyperparameters**: `random_state=42` for reproducibility.

## 4. Performance Metrics
- **Accuracy**: 82.44%
- **ROC AUC**: 0.8841 (High diagnostic ability)
- **Precision/Recall**: 
    - **Recall for Class 1 (Disease)**: 0.90 (High sensitivity is crucial for medical diagnosis).
    - **Precision for Class 1**: 0.78.
- **Confusion Matrix**: Shows 76 True Negatives and 93 True Positives.

## 5. Key Insights from Visualizations
- **Coefficients**: `Chest_Pain_Type` and `ST_Slope` show significant positive correlations with heart disease, while `Major_Vessels` and `Sex` show strong negative correlations.
- **Feature Distribution**: Visual analysis confirms distinct distributions for features like `Max_Heart_Rate` and `ST_Depression` between healthy and diseased groups.
- **PR Curve**: The Precision-Recall AUC of 0.88 indicates robust performance even when balancing precision and recall.

## 6. Conclusion
The model is highly effective at identifying positive cases (90% recall), making it a useful screening tool. Future work could involve testing non-linear models like Random Forests or Gradient Boosting to see if accuracy can be further improved.