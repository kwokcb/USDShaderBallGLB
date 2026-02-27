# Create and enter a new directory
mkdir StandardShaderBall
cd StandardShaderBall

# Initialize a new git repository
git init

# Add the remote repository
git remote add origin https://github.com/usd-wg/assets.git

# Enable sparse-checkout
git config core.sparseCheckout true

# Specify the folder you want
echo "full_assets/StandardShaderBall/*" >> .git/info/sparse-checkout

# Pull the files from the remote (usually the main/master branch)
git pull origin main