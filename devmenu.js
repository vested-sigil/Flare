const Parse = require('parse/node');
// The initialization setup of Parse should be the same as previously defined in index.js

// Calling `developerMenu` to perform a 'create' action
Parse.Cloud.run('developerMenu', { action: 'create' }).then((result) => {
  console.log(result);
}).catch((error) => {
  console.error(error);
});