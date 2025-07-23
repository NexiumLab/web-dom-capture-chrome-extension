const path = require('path');

module.exports = {
  mode: 'production', // Use 'development' for easier debugging
  entry: {
    popup: './popup.js',
    background: './background.js',
  },
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: '[name].bundle.js',
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
      },
    ],
  },
}; 