import os
from flask import Flask, request, jsonify
import os.path
import  constants
import fnmatch

app = Flask(__name__)

SECRET_KEY = os.environ.get("SECRET_KEY")


def get_port():
    port = os.environ.get("PORT")
    if not port:
        port = 4000
    return 4000


@app.route("/")
def index():
    return jsonify({'hello': 'world'})


@app.route("/env")
def evn_shows():
    try:
        if SECRET_KEY:
            return "Remote address : " + SECRET_KEY
        else:
            return 'Remote address not set'
    except Exception as e:
        return jsonify({'error': str(e),
                        'status': 500,
                        'message': 'Something went wrong'})


@app.route('/files', methods=['POST'])
def create_file():
    try:
        request_data = request.get_json()
        try:
            name = request_data['name']
            data = request_data['data']
            name_of_file = name + '.txt'
        except Exception as e:
            return jsonify({
                'error': str(e),
                'status': 400,
                'message': 'Invalid input/ empty value'})
        if not name or not data:
            return jsonify({
                'status': 400,
                'message': 'Invalid input/ empty value'})
        else:
            # go to test folder
            filepath = os.path.join(constants.FILE_PATH, name_of_file)
            if not os.path.exists(constants.FILE_PATH):
                os.umask(0)
                os.makedirs(constants.FILE_PATH, mode=0o777)
            os.chdir(constants.FILE_PATH)
            # check file exist
            if os.path.isfile(name_of_file):
                return jsonify({
                    'name': name_of_file,
                    'status': 409,
                    'message': 'file name already exist'})
            else:
                try:
                    f = open(filepath, "w")
                    f.writelines([data])
                except Exception as e:
                    raise Exception(str(e))
                finally:
                    print("-------in finally---------------")
                    f.close()
                return jsonify({
                    'name': name_of_file,
                    'status': 200,
                    'message': 'successfully created'})
    except Exception as e:
        return jsonify({'error': str(e),
                        'status': 500,
                        'message': 'Something went wrong'})


@app.route('/files', methods=['GET'])
def get_all_files():
    try:
        os.chdir(constants.FILE_PATH)
        files = fnmatch.filter(os.listdir(), '*.txt')
        return jsonify({
            'files': files,
            'status': 200,
            'message': 'successfully listed'})
    except Exception as e:
        return jsonify({'error': str(e),
                        'status': 500,
                        'message': 'Something went wrong'})


@app.route('/files/<string:name>', methods=['GET'])
def get_file_content(name):
    try:
        os.chdir(constants.FILE_PATH)
        file = os.path.exists(name + ".txt")
        try:
            if not file:
                return jsonify({
                    'name': name + ".txt",
                    'status': 404,
                    'message': 'file not exist'})
            else:
                f = open(name + ".txt")
                content = str(f.read())
                f.close()
                return jsonify({
                    "file_name": name + ".txt",
                    'content': content,
                    'status': 200,
                    'message': 'successfully updated'})

        except Exception as e:
            return jsonify({'error': str(e),
                            'status': 404,
                            'message': 'Something went wrong'})

    except Exception as e:
        return jsonify({'error': str(e),
                        'status': 500,
                        'message': 'Something went wrong'})


@app.route('/files/<string:name>', methods=['DELETE'])
def delete_file(name):
    try:
        os.chdir(constants.FILE_PATH)
        file = os.path.exists(name+".txt")
        try:
            if not file:
                return jsonify({
                    'name': name + ".txt",
                    'status': 404,
                    'message': 'file not exist'})
            else:
                os.remove(name+".txt")
                return jsonify({
                    'id': name,
                    'status': 200,
                    'message': 'successfully deleted'})

        except Exception as e:
            return jsonify({'error': str(e),
                            'status': 404,
                            'message': 'Something went wrong'})

    except Exception as e:
        return jsonify({'error': str(e),
                        'status': 500,
                        'message': 'Something went wrong'})


@app.route('/files/<string:name>', methods=['PATCH'])
def patch_file(name):
    try:
        os.chdir(constants.FILE_PATH)
        file = os.path.exists(name+".txt")
        request_data = request.get_json()
        try:
            rename = request_data['name']
            if not file:
                return jsonify({
                    'name': name + ".txt",
                    'status': 404,
                    'message': 'file not exist'})
            else:
                os.rename(name + ".txt", rename+".txt")
                return jsonify({
                    'id': name,
                    'status': 200,
                    'message': 'successfully updated file name'})

        except Exception as e:
            return jsonify({'error': str(e),
                            'status': 404,
                            'message': 'Something went wrong'})

    except Exception as e:
        return jsonify({'error': str(e),
                        'status': 500,
                        'message': 'Something went wrong'})


@app.route('/files/<string:name>', methods=['PUT'])
def update_file(name):
    try:
        os.chdir(constants.FILE_PATH)
        file = os.path.exists(name+".txt")
        request_data = request.get_json()
        try:
            data = request_data['data']
            if not file:
                return jsonify({
                    'name': name + ".txt",
                    'status': 404,
                    'message': 'file not exist'})
            else:
                f = open(name + ".txt", "w")
                f.write(data)
                f.close()
                return jsonify({
                    'id': name,
                    'status': 200,
                    'message': 'successfully updated'})

        except Exception as e:
            return jsonify({'error': str(e),
                            'status': 404,
                            'message': 'Something went wrong'})

    except Exception as e:
        return jsonify({'error': str(e),
                        'status': 500,
                        'message': 'Something went wrong'})


if __name__ == "__main__":
    print("URLs: ", app.url_map)
    app.run(debug=True, host='0.0.0.0', port=get_port())
