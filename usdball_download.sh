# Create and enter a new directory
echo "Making folder called StandardShaderBall"
mkdir StandardShaderBall
cd StandardShaderBall

# Initialize a new git repository
echo "Initializing git repository"
git init

# Add the remote repository
echo "Adding remote repository: https://github.com/usd-wg/assets.git"
git remote add origin https://github.com/usd-wg/assets.git

# Enable sparse-checkout
echo "Configuring sparse checkout"
git config core.sparseCheckout true

# Specify the folder you want
echo "Want only: full_assets/StandardShaderBall/*"
echo "full_assets/StandardShaderBall/*" >> .git/info/sparse-checkout

# Pull the files from the remote
ehoc "Pulling the specified files from the remote repository"
git pull origin main