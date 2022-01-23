const path = require('path');

module.exports = {
  entry: './assets/index.js',  // path to our input file
  output: {
    filename: 'index-bundle.js',  // output bundle file name
    path: path.resolve(__dirname, './app/static'),  // path to our static directory
  },
  module: {
    rules: [
        {
          test: /\.(js|jsx)$/,
          exclude: /node_modules/,
          loader: "babel-loader",
          options: { presets: ["@babel/preset-env", "@babel/preset-react"] }
        },
        {
          test: /\.css$/i,
          use: ["style-loader", "css-loader"],
        },
    ],
  }
};