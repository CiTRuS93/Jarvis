from flask import Flask, request, jsonify
from jarviscli.ui.cmd_interpreter import CmdInterpreter
from jarviscli.language import snips
from jarviscli.main import build_plugin_manager
from jarviscli.jarvis import Jarvis

app = Flask(__name__)

jarvis_dict = {}

@app.route('/command')
def command():
    uid = int(request.args.get('id'))
    command = request.args.get('command')
    
    cmd_interpreter = jarvis_dict[uid]
    command = " ".join(command).strip()
    
    
    #override the stdout so every print will be sent to the client
    with io.StringIO() as buf, redirect_stdout(buf):
        cmd_interpreter.executor(command)
        output = buf.getvalue()
    return jsonify({'response':output})


@app.route('/connect')
def connect():
    # language_parser = default.DefaultLanguageParser()
    language_parser = snips.LanguageParser()
    plugin_manager = build_plugin_manager()
    jarvis = Jarvis(language_parser, plugin_manager)
    cmd_interpreter = CmdInterpreter(jarvis)


    #using general index as user_id, later can be switched to tokens
    jarvis_dict[len(jarvis_dict)] = cmd_interpreter
    return jsonify({'user_id': len(jarvis_dict) - 1})


if __name__ == '__main__':
    app.run(threaded=True)
