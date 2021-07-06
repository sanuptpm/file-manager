import os
from flask import Flask, request, jsonify
import os.path
import fnmatch
from src.constants import cmn_constant

app = Flask(__name__)
f = None


def get_port():
    port = os.environ.get("PORT")
    if not port:
        port = 4000
    return port


def get_secret_key():
    key = os.environ.get("SECRET_KEY")
    if not key:
        key = 'SECRET_KEY'
    return key


@app.route("/")
def index():
    return jsonify({'hello': 'world'})


@app.route("/env")
def get_env():
    try:
        return "Remote address : " + get_secret_key()
    except Exception as e:
        return jsonify(error=str(e), message="Something went wrong"), 500


def get_request():
    return request.get_json()


@app.route('/files', methods=['POST'])
def create_file():
    try:
        request_data = get_request()
        try:
            name = request_data['name']
            data = request_data['data']
            name_of_file = name + '.txt'
        except Exception as e:
            return jsonify(error=str(e), message="Invalid input/ empty value"), 400
        # go to test folder
        filepath = os.path.join(cmn_constant.FILE_PATH, name_of_file)
        if not os.path.exists(cmn_constant.FILE_PATH):
            os.umask(0)
            os.makedirs(cmn_constant.FILE_PATH, mode=0o777)
        os.chdir(cmn_constant.FILE_PATH)
        # check file exist
        if os.path.isfile(name_of_file):
            return jsonify(name=str(name_of_file), message="File name already exist"), 409
        else:
            try:
                f = open(filepath, "w")
                f.writelines([data])
            except Exception as e:
                raise Exception(str(e))
            finally:
                f.close()
            return jsonify(name=str(name_of_file), message="Successfully created"), 200
    except Exception as e:
        return jsonify(error=str(e), message="Something went wrong"), 500


@app.route('/files', methods=['GET'])
def get_all_files():
    try:
        os.chdir(cmn_constant.FILE_PATH)
        try:
            files = fnmatch.filter(os.listdir(), '*.txt')
        except Exception as e:
            raise Exception(str(e))
        return jsonify(files=str(files), message="Successfully listed"), 200
    except Exception as e:
        return jsonify(error=str(e), message="Something went wrong"), 500


@app.route('/files/<string:name>', methods=['GET'])
def get_file_content(name):
    try:
        os.chdir(cmn_constant.FILE_PATH)
        try:
            file = open(name + ".txt")
            content = str(file.read())
        except Exception as e:
            return jsonify(error=str(e), message="File not exist"), 404
        finally:
            if file is not None:
                file.close()
            return jsonify(name=str(name + ".txt"), content=str(content), message="Successfully listed"), 200
    except Exception as e:
        return jsonify(error=str(e), message="Something went wrong"), 500


@app.route('/files/<string:name>', methods=['DELETE'])
def delete_file(name):
    try:
        os.chdir(cmn_constant.FILE_PATH)
        try:
            os.remove(name + ".txt")
            return jsonify(name=str(name), message="Successfully deleted"), 200
        except Exception as e:
            return jsonify(error=str(e), message="File not exist"), 404
    except Exception as e:
        return jsonify(error=str(e), message="Something went wrong"), 500


@app.route('/files/<string:name>', methods=['PATCH'])
def patch_file(name):
    try:
        os.chdir(cmn_constant.FILE_PATH)
        try:
            request_data = get_request()
            rename = request_data['name']
            os.rename(name + ".txt", rename + ".txt")
            return jsonify(name=str(name), message="successfully updated file name"), 200
        except Exception as e:
            return jsonify(error=str(e), message="file name not exist"), 404
    except Exception as e:
        return jsonify(error=str(e), message="Something went wrong"), 500


@app.route('/files/<string:name>', methods=['PUT'])
def update_file(name):
    try:
        os.chdir(cmn_constant.FILE_PATH)
        if os.path.exists(cmn_constant.FILE_PATH + '/' + name + '.txt'):
            f = None
            try:
                request_data = get_request()
                data = request_data['data']
                f = open(name + ".txt", "w")
                f.write(data)
            except Exception as e:
                raise Exception(str(e))
            finally:
                if f is not None:
                    f.close()
                return jsonify(name=str(name), message="successfully updated file name"), 200
        else:
            return jsonify(message="file name not exist"), 404
    except Exception as e:
        return jsonify(error=str(e), message="Something went wrong"), 500


if __name__ == "__main__":
    print("URLs: ", app.url_map)
    app.run(debug=True, host='0.0.0.0', port=get_port())
