from flask import Flask, jsonify, request

stores = {
    '101': {'name': 'John Doe', 'age': 18, 'class': '10A'},
    '102': {'name': 'Jane Smith', 'age': 17, 'class': '9B'},
    # Add more students here...
}

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello, World :)'})

@app.route('/trigger_report', methods=['GET'])
def trigger_report():
    return jsonify({'action': 'Trigger Report!'})

@app.route('/get_report', methods=['GET'])
def get_report():
    return jsonify({'101': stores['101']})

@app.route('/get_report/<string:report_id>', methods=['GET'])
def get_student_by_report_id(report_id):
    if report_id in stores:
        return jsonify(stores[report_id])
    else:
        return jsonify({'error': 'Student not found'}), 404

if __name__ == '__main__':
    app.run()