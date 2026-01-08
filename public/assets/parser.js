const fs = require('fs');
const path = require('path');

class Parser {
  constructor(filePath) {
    this.filePath = filePath;
    this.data = [];
  }

  async readData() {
    try {
      const content = await fs.promises.readFile(this.filePath, 'utf8');
      const lines = content.split('\n');
      lines.forEach((line) => {
        const [date, amount, description] = line.split(',');
        if (date && amount && description) {
          this.data.push({
            date: new Date(date.trim()),
            amount: parseFloat(amount.trim()),
            description: description.trim(),
          });
        }
      });
    } catch (error) {
      console.error(`Error reading file: ${error.message}`);
    }
  }

  async parseData() {
    await this.readData();
    return this.data;
  }
}

module.exports = Parser;