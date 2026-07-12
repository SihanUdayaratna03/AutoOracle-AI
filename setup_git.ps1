git init

# Commit 1
Set-Content -Path .gitignore -Value "venv/`n__pycache__/`n.ipynb_checkpoints/"
git add .gitignore
git commit -m "Initial commit: Add .gitignore to exclude virtual environments"

# Commit 2
Set-Content -Path README.md -Value "# AutoOracle-AI`n`nA Machine Learning project for predicting used car prices based on various features like age, mileage, and transmission type.`n"
git add README.md
git commit -m "docs: Create project README"

# Commit 3
git add requirements.txt
git commit -m "chore: Add project dependencies for ML models and data processing"

# Commit 4
git add car_data.csv
git commit -m "data: Add historical car pricing dataset"

# Commit 5
git add car-price-prediction.ipynb
git commit -m "feat: Initialize Jupyter notebook with data exploration and model setup"

# Commit 6
Add-Content -Path README.md -Value "`n## Dataset`nThe dataset contains features such as:`n- Selling Price`n- Present Price`n- Kms Driven`n- Fuel Type`n- Seller Type`n- Transmission`n- Owner`n"
git add README.md
git commit -m "docs: Document dataset features in README"

# Commit 7
Add-Content -Path README.md -Value "`n## Models Used`nThe following models are evaluated:`n1. Linear Regression`n2. Lasso Regression`n3. Random Forest Regressor`n"
git add README.md
git commit -m "docs: Update README with machine learning models used"

# Commit 8
Add-Content -Path README.md -Value "`n## Setup Instructions`n1. Clone the repository.`n2. Run ``pip install -r requirements.txt```n3. Open the Jupyter Notebook to run the predictions.`n"
git add README.md
git commit -m "docs: Add local setup and installation instructions"

# Commit 9
$licenseText = @"
MIT License

Copyright (c) 2024 SihanUdayaratna03

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the ""Software""), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED ""AS IS"", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"@
Set-Content -Path LICENSE -Value $licenseText
git add LICENSE
git commit -m "chore: Add MIT License"

# Push to remote
git remote add origin https://github.com/SihanUdayaratna03/AutoOracle-AI.git
git branch -M main
git push -u origin main
