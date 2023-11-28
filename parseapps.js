class ParseApps {
    constructor() {
      this.create = {
        path: '/parse-apps/create',
        method: 'POST',
        summary: 'Create a new Parse App',
        request: {
          parameters: {},
          requestBody: {
            appName: {
              type: 'string',
              description: 'The name of the Parse App to create'
            },
            appTemplate: {
              type: 'string',
              description: 'Optional template to use when creating the app',
              default: 'blank'
            }
          }
        },
        response: {
          '200': {
            description: 'Parse App created successfully',
            content: {
              applicationId: 'string',
              clientKey: 'string',
              restApiKey: 'string',
              masterKey: 'string'
            }
          },
          '400': {
            description: 'Invalid request'
          },
          '500': {
            description: 'Server error'
          }
        },
        schemas: {
          CreateParseAppRequest: {
            type: 'object',
            properties: {
              appName: {
                type: 'string'
              },
              appTemplate: {
                type: 'string'
              }
            },
            required: ['appName']
          }
        }
      };
    }
  }
  
  module.exports = ParseApps;
  