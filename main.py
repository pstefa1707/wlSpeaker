from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from mediaPlayer import Player


app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

player = Player()

@app.route('/')
def index():
	return render_template("index.html", current=player.current, queue=player.queue, play=player.status)

@app.errorhandler(404)
def page_not_found(error):
	return "404 page doesnt exist!", 404

@socketio.on("newConnection")
def handle_newConnection():
	print("Recieved a new connection!")

@socketio.on("control")
def handle_control(data):
	if data == "play_pause":
		if not player.status:
			player.play()
			emit('songChange', [player.current.url, player.current.song])
		else:
			player.pause()
	elif data == "skip":
		player.skip()
		emit('queueChange', player.queue)
		emit('songChange', [player.current.url, player.current.song])
	else:
		player.previous()
		emit('queueChange', player.queue)
		emit('songChange', [player.current.url, player.current.song])
	emit('statusChange', player.status)

@socketio.on("appendQueue")
def handle_queue(data):
	player.addToQueue(data)
	emit('queueChange', player.queue)

if __name__ == '__main__':
	socketio.run(app, log_output=True, host='0.0.0.0', port="80")