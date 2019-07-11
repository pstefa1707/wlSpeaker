import vlc
import S2Y
import pafy
import traceback
import multiprocessing

class Current():
	def __init__(self):
		self.prevSong = None
		self.prevUrl = None
		self.song = None
		self.url = None


class Player():
	def __init__(self):
		self.status = False
		self.queue = {}
		self.queue['urls'] = []
		self.queue['songs'] = []
		self.current = Current()
		self.Instance = vlc.Instance()
		self.player = self.Instance.media_player_new()

	def addToQueue(self, url):
		try:
			self.queue['songs'] = S2Y.getTracks(url)
			self.queue['urls'] = S2Y.songToYoutubeQuery(self.queue['songs'])
			with multiprocessing.Pool() as pool:
				temp = pool.map(S2Y.searchYoutube, self.queue['urls'])
			self.queue['urls'].append(temp)
			self.queue['urls'] = [item for sublist in self.queue['urls'] for item in sublist if len(item) > 1]
			return True
		except Exception:
			traceback.print_exc()
			print("Error adding songs to queue.")
			return False

	def play(self):
		try:
			if self.current.url == None:
				self.playInit()
			else:
				self.player.play()
				self.status = True
			return True
		except:
			traceback.print_exc()
			return False
	
	def playInit(self):

		if len(self.queue['urls']) > 0:
			self.status = True;
			self.current.prevUrl = self.current.url
			self.current.prevSong = self.current.song
			self.current.url = self.queue['urls'].pop(0)
			self.queue['songs'].pop(0)
			video = pafy.new(self.current.url)
			self.current.song = video.title
			bestaudio = video.getbestaudio()
			Media = self.Instance.media_new(bestaudio.url)
			Media.get_mrl()
			self.player.set_media(Media)
			self.play()
			return True
		return False

	def skip(self):
		return self.playInit()

	def pause(self):
		try:
			self.player.stop()
			self.status = False
			return True
		except:
			return False

	def currentSong(self):
		return self.current

	def previous(self):
		if (self.current.prevSong == None):
			return False
		else:
			self.queue['urls'].insert(0, self.current.url)
			self.queue['songs'].insert(0, self.current.song)
			self.current.url = self.current.prevUrl
			self.current.song = self.current.prevSong
			self.current.prevSong = None
			self.current.prevUrl = None
			video = pafy.new(self.current.url)
			self.current.song = video.title
			bestaudio = video.getbestaudio()
			Media = self.Instance.media_new(bestaudio.url)
			Media.get_mrl()
			self.player.set_media(Media)
			self.play()
		return True