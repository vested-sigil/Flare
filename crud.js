const Parse = require('parse/node');

class CRUD {
  static async create(className, data) {
    const ParseObject = Parse.Object.extend(className);
    const parseObject = new ParseObject();
    Object.keys(data).forEach(key => {
      parseObject.set(key, data[key]);
    });
    try {
      const result = await parseObject.save();
      return result;
    } catch (error) {
      throw new Error('Error creating object: ' + error.message);
    }
  }

  static async read(className, criteria = {}) {
    const parseQuery = new Parse.Query(className);
    Object.entries(criteria).forEach(([key, value]) => {
      parseQuery.equalTo(key, value);
    });
    try {
      const results = await parseQuery.find();
      return results;
    } catch (error) {
      throw new Error('Error reading objects: ' + error.message);
    }
  }

  static async update(className, objectId, data) {
    const parseQuery = new Parse.Query(className);
    try {
      const parseObject = await parseQuery.get(objectId);
      Object.keys(data).forEach(key => {
        parseObject.set(key, data[key]);
      });
      const result = await parseObject.save();
      return result;
    } catch (error) {
      throw new Error('Error updating object: ' + error.message);
    }
  }

  static async del(className, objectId) {
    const parseQuery = new Parse.Query(className);
    try {
      const parseObject = await parseQuery.get(objectId);
      const result = await parseObject.destroy();
      return result;
    } catch (error) {
      throw new Error('Error deleting object: ' + error.message);
    }
  }
}

module.exports = CRUD;