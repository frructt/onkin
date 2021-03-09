import {Component, OnChanges, OnDestroy, OnInit, SimpleChanges} from '@angular/core';
import {AuthenticationService, SocketioService, VideoService} from '@app/_services';
import { ChatMessageDto } from '@app/_models'
import {HttpResponse} from '@angular/common/http';
import {NgForm} from '@angular/forms'
import {User} from '@app/_models';
import {map, switchMap} from 'rxjs/operators';
import { RoomService } from '@app/_services';


@Component({
  selector: 'app-vdo-player',
  templateUrl: './player.component.html',
  styleUrls: ['./player.component.scss']
})

export class PlayerComponent implements OnInit, OnChanges, OnDestroy {

  // socket: SocketioService;
  currentUser: string;
  anotherUser: string;
  // videoName: string;
  videoItem;
  data;
  video;
  // video = document.createElement('video');
  isPlaying: boolean;
  // message: string;
  newMessage = '';
  messages: ChatMessageDto[] = [];
  roomId: string;

  videoControls;
  playpause;
  stop;
  mute;
  volinc;
  voldec
  progress;
  progressBar;
  fullscreen;
  videoContainer;


  constructor(private videoService: VideoService,
              private authenticationService: AuthenticationService,
              private socket: SocketioService) {
    socket.connect();
    this.currentUser = this.authenticationService.currentUserValue.username;
    this.anotherUser = this.authenticationService.currentUserValue.username;
    this.isPlaying = false;
    this.roomId = this.authenticationService.currentUserValue.roomId;
  }

  ngOnInit() {
    this.videoService.getVideo()
      .pipe(
        switchMap(data =>
          this.videoService.streamVideo(data.fileName)
            .pipe(
              map(response => (
                this.videoItem = {
                name: 'video name',
                src: response.url,
                type: 'video/mp4'
                }))
            )
      )
    ).subscribe(result => console.log('merged: ', result))

    this.videoContainer = document.getElementById('videoContainer');
    this.video = document.getElementById('videoId');
    this.video.controls = false;
    this.videoControls = document.getElementById('player-controls');

    this.playpause = document.getElementById('playpause');
    this.stop = document.getElementById('stop');
    this.mute = document.getElementById('mute');
    this.volinc = document.getElementById('volinc');
    this.voldec = document.getElementById('voldec');
    this.progress = document.getElementById('progress');
    this.progressBar = document.getElementById('progress-bar');
    this.fullscreen = document.getElementById('fs');

    // this.playpause.addEventListener('click', this.playVid());
    // this.mute.addEventListener('click', this.muteVideo());
    // this.volinc.addEventListener('click', this.volumeInc());
    // this.voldec.addEventListener('click', this.volumeDec());
    // this.video.addEventListener('loadedmetadata', this.setDuration());
    // this.video.addEventListener('timeupdate', this.progressBarUpdate());
    //
    // var fullScreenEnabled = !!(document.fullscreenEnabled);
    // if (!fullScreenEnabled) {
    //   this.fullscreen.style.display = 'none';
    // }
    // this.fullscreen.addEventListener('click', this.changeFullscreen());

    // document.addEventListener('fullscreenchange', this.documentChangeFullScreenListener());

    this.videoControls.setAttribute('data-state', 'visible');
    var supportsProgress = (document.createElement('progress').max != undefined);
    if (!supportsProgress) this.progress.setAttribute('data-state', 'fake');

    // function changeButtonState(type) {
    //   if (type == 'playpause') {
    //     if (this.video || this.video.ended) {
    //       this.playpause.setAttribute('data-state', 'play');
    //     }
    //     else {
    //       this.playpause.setAttribute('data-state', 'pause');
    //     }
    //   }
    //   else if (type == 'mute') {
    //     this.mute.setAttribute('data-state', this.video.muted ? 'unmute' : 'mute');
    //   }
    // }

    // this.video.addEventListener('play', function () {
    //   this.changeButtonState('playpause')
    // }, false);

    // this.video.addEventListener('play', this.changeButtonState('playpause'), false);


    // this.video.addEventListener('pause', this.changeButtonState('playpause'), false);
    // this.mute.addEventListener('click', this.muteListener());
    // this.playpause.addEventListener('click', this.onPlayPauseEvent());
    // this.video.addEventListener('volumechange', this.checkVolume(''), false);
    // this.progress.addEventListener('click', this.progressEventListener());

    // this.changeVolume();
    // this.fullScreenVid();
    this.onPauseEvent();
    this.onPlayEvent();
    this.changeVideoPositionEvent();
    this.BroadcastMessages();

    this.openChat();
  }

  ngAfterViewInit() {

  }

  ngOnChanges(changes: SimpleChanges) {
    // this.SendMessage()
    // listen chat messages
    // this.BroadcastMessages()
  }

  ngOnDestroy() {}

  BroadcastMessages() {
    this.socket.socketInstance.on('message', (data) => {
     if (data) {
        if (data.roomId === this.roomId) {
            const chatMessageDto = new ChatMessageDto(data.username, data.msg, data.roomId, data.time_stamp)
            this.messages.push(chatMessageDto)
        } else {
            // printSysMsg(data.msg)
        }
      }
    });
  }

  sendMessage(sendForm: NgForm) {
     // const chatMessageDto = new ChatMessageDto(this.currentUser, sendForm.value.newMessage, '')
     this.socket.socketInstance.emit('message', {username: this.currentUser, msg: sendForm.value.newMessage, roomId: this.roomId});
     sendForm.controls.newMessage.reset();
  }

  // sendMessage(sendForm: NgForm) {
  //   console.log({username: this.currentUser, msg: sendForm.value.message})
  // }

  // Play video function
  playVid() {
    if (this.video.paused && !this.isPlaying) {
        console.log('start playing for user ' + this.currentUser);
        this.video.play();
    } else {
        console.log('video is already played for user ' + this.currentUser);
    }
  }


  playVideo() {
    this.video.play();
    this.isPlaying = true;
    if (this.anotherUser === this.currentUser){
        console.log('video is playing from user ' + this.currentUser);
        this.socket.socketInstance.emit('play-video', {username: this.currentUser, roomId: this.roomId});
    } else {
        console.log(' ' + this.anotherUser + ' != ' + this.currentUser);
        this.anotherUser = this.currentUser;
    }
  }

  onPlayEvent() {
    this.socket.socketInstance.on('onplay event', data => {
      if (data.roomId === this.roomId) {
          this.anotherUser = data.username
          this.playVid();
      }
    });
  }

  // Pause video function
  pauseVid() {
    if (!this.video.paused && this.isPlaying) {
      console.log('start stopping for user ' + this.currentUser);
      this.video.pause();
    } else {
      console.log('video is already stopped for user ' + this.currentUser);
    }
  }

  pauseVideo() {
    this.video.pause();
    this.isPlaying = false;
    if (this.anotherUser === this.currentUser){
      if (!this.video.seeking) {  // if seeking don't send pause event to server
        console.log('video is paused by user ' + this.currentUser);
        this.socket.socketInstance.emit('pause-video', {username: this.currentUser, roomId: this.roomId});
      }
    } else {
      console.log(' ' + this.anotherUser + ' != ' + this.currentUser);
      this.anotherUser = this.currentUser;
    }
  }

  onPauseEvent() {
    this.socket.socketInstance.on('onpause event', data => {
      if (data.roomId === this.roomId) {
          this.anotherUser = data.username
          this.pauseVid();
      }
    });
  }

  onPlayPauseEvent(e) {
    if (this.video.paused || this.video.ended) this.playVideo();
    else this.pauseVideo();
  }

  onSeeked() {
    if (this.anotherUser === this.currentUser){
      console.log(this.video.currentTime);
      this.socket.socketInstance.emit('change-video-position',
        {current_position: this.video.currentTime, username: this.currentUser, roomId: this.roomId});
    } else {
      console.log(' ' + this.anotherUser + ' != ' + this.currentUser);
      this.anotherUser = this.currentUser;
    }
  }

  changeVideoPositionEvent() {
    this.socket.socketInstance.on('change video position event', data => {
        console.log('difference in positions (sec): ' + Math.abs((data.current_position - this.video.currentTime)))
        if ((this.video.currentTime !== data.current_position) && data.username !== this.currentUser && data.roomId === this.roomId) {
            this.anotherUser = data.username;
            console.log('video.currentTime: ' + this.video.currentTime + ' current_position: ' + data.current_position);
            this.video.currentTime = data.current_position;
        }
        else {
            this.anotherUser = data.username;
            console.log('position in the same');
        }
    })
  }

  progressEventListener(e) {
    let pos = (e.pageX - (e.offsetLeft + e.offsetParent.offsetLeft)) / e.offsetWidth;
    this.video.currentTime = pos * this.video.duration;
  }

  checkVolume(dir) {
    if (dir != '') {
      let currentVolume = Math.floor(this.video.volume * 10) / 10;
      if (dir === '+') {
        if (currentVolume < 1) this.video.volume += 0.1;
      }
      else if (dir === '-') {
        if (currentVolume > 0) this.video.volume -= 0.1;
      }

      this.video.muted = currentVolume <= 0;
    }
      this.changeButtonState('mute');
  }

  muteListener() {
    this.video.muted = !this.video.muted;
    this.changeButtonState('mute');
  }

  changeButtonState(type) {
    if (type == 'playpause') {
        if (this.video.paused || this.video.ended) {
          this.playpause.setAttribute('data-state', 'play');
        }
        else {
          this.playpause.setAttribute('data-state', 'pause');
        }
      }
      else if (type == 'mute') {
        this.mute.setAttribute('data-state', this.video.muted ? 'unmute' : 'mute');
      }
  }

  documentChangeFullScreenListener() {
    this.setFullScreenData(!!(document.fullscreen || document.fullscreenElement));
  }

  skipAhead(e) {
    var pos = (e.pageX - e.offsetLeft) / e.offsetWidth;
    this.video.currentTime = pos * this.video.duration;
  }

  changeFullscreen() {
    this.handleFullScreen();
  }

  handleFullScreen() {
    if (this.isFullScreen()) {
      if (document.exitFullscreen) document.exitFullscreen();
      this.setFullScreenData(false);
    }
    else {
      if (this.videoContainer.requestFullscreen) this.videoContainer.requestFullscreen();
      this.setFullScreenData(true);
    }
  }

  setFullScreenData (state) {
    this.videoContainer.setAttribute('data-fullscreen', !!state);
  }

  isFullScreen() {
    return !!(document.fullscreen || document.fullscreenElement);
  }

  progressBarUpdate() {
    if (!this.progress.getAttribute('max')) this.progress.setAttribute('max', this.video.duration);
    this.progress.value = this.video.currentTime;
    this.progressBar.style.width = Math.floor((this.video.currentTime / this.video.duration) * 100) + '%';
  }

  setDuration() {
    this.progress.setAttribute('max', this.video.duration);
  }

  volumeInc() {
    this.alterVolume('+');
  }

  volumeDec() {
    this.alterVolume('-');
  }

  alterVolume(dir) {

    this.checkVolume(dir);

    // var currentVolume = Math.floor(this.video.volume * 10) / 10;
    // if (dir === '+') {
    //   if (currentVolume < 1) this.video.volume += 0.1;
    // }
    // else if (dir === '-') {
    //   if (currentVolume > 0) this.video.volume -= 0.1;
    // }
  }

  muteVideo() {
    this.video.muted = !this.video.muted;
  }

  changeVolume() {
    this.video.volume = document.getElementById("change_vol").nodeValue;
  }

  fullScreenVid() {
    this.video.fullscreenchange;
  }


  openChat () {
    document.getElementById('chatForm').style.display = 'block';
    document.getElementById('showChat').style.display = 'none';
  }

  closeChat() {
      document.getElementById('chatForm').style.display = 'none';
      document.getElementById('showChat').style.display = 'block';

  }
}
