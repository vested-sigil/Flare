require('dotenv').config();
const Parse = require('parse/node');

// Initialize Parse
Parse.initialize(process.env.BACK4APP_APP_ID, process.env.BACK4APP_JAVASCRIPT_KEY, process.env.BACK4APP_MASTER_KEY);
Parse.serverURL = 'https://parseapi.back4app.com';

const getSchema = async () => {
  // Use the master key for fetching schema information
  Parse.Cloud.useMasterKey();
  
  try {
    const response = await Parse._request('GET', 'schemas', {}, { useMasterKey: true });
    console.log(JSON.stringify(response, null, 2));
  } catch (error) {
    console.error('Error retrieving schema:', error);
  }
};

getSchema();