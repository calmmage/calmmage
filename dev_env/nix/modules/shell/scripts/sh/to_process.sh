function add_alias() {
    # Create .zshrc.new if it doesn't exist
    touch ~/.zshrc.new
    
    echo "" >> ~/.zshrc.new
    echo "# $3" >> ~/.zshrc.new
    echo "alias $1=\"$2\"" >> ~/.zshrc.new
    source ~/.zshrc.new
}