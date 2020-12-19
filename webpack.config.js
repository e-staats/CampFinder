// This library allows us to combine paths easily
const path = require('path');

module.exports = {
   entry: {
      app: path.resolve(__dirname, 'static/js/react-app', 'index.js'),
      searchList: path.resolve(__dirname, 'static/js/react-app/account', 'account.js'),
      preferences: path.resolve(__dirname, 'static/js/react-app/userPreferences', 'userPreferences.js'),
   },
   output: {
      path: path.resolve(__dirname, 'static/js/compiled_js'),
      filename: '[name].js',
   },
   resolve: {
      extensions: ['.js', '.jsx']
   },
   module: {
      rules: [
         { test: /\.jsx$/, use: 'babel-loader' },
         { test: /\.js$/, use: 'babel-loader' }
      ]
   }
};