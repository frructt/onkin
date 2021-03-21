import {Component, OnChanges, OnDestroy, OnInit, SimpleChanges} from '@angular/core';
import {AuthenticationService, SocketioService, VideoService} from '@app/_services';
import { ChatMessageDto } from '@app/_models'
import {HttpResponse} from '@angular/common/http';
import {NgForm} from '@angular/forms'
import {User} from '@app/_models';
import {map, min, switchMap} from 'rxjs/operators';
import { RoomService } from '@app/_services';
import { NgScrollbarModule } from 'ngx-scrollbar';


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
  playbackBar;
  playPauseBtn;
  volumeUpMuteBtn;
  onOffFullScreenBtn;
  videoFrame;
  currentTime;
  totalTime;
  // video = document.createElement('video');
  isPlaying: boolean;
  // message: string;
  newMessage = '';
  messages: ChatMessageDto[] = [];
  roomId: string;
  dateToday: number


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

    this.video = document.getElementById('videoId');
    this.playbackBar = document.querySelector('.playback_bar');
    this.playPauseBtn = document.getElementById('play-pause');
    this.volumeUpMuteBtn = document.getElementById('up-mute');
    this.onOffFullScreenBtn = document.getElementById('on-off');
    this.videoFrame = document.querySelector('.c_video');
    this.currentTime = '00:00:00';
    this.totalTime = '00:00:00';


    this.onPauseEvent();
    this.onPlayEvent();
    this.changeVideoPositionEvent();
    this.BroadcastMessages();

    this.openChat();
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
            data.timestamp = this.getDate()
            const chatMessageDto = new ChatMessageDto(data.username, data.msg, data.roomId, data.timestamp)
            this.messages.push(chatMessageDto)
        } else {
            // printSysMsg(data.msg)
        }
      }
    });
  }

  getDate() {
    return Date.now();
  }

  sendMessage(sendForm: NgForm) {
     // const chatMessageDto = new ChatMessageDto(this.currentUser, sendForm.value.newMessage, '')
    if (sendForm.value.newMessage.trim().length) {
      this.socket.socketInstance.emit('message', {username: this.currentUser, msg: sendForm.value.newMessage, roomId: this.roomId});
      sendForm.controls.newMessage.reset();
    }
  }

  // player functions
  togglePlayPause($event: MouseEvent) {
    if (this.video.paused) {
      this.playPauseBtn.className = 'pause';
      this.video.play()
    }
    else {
      this.playPauseBtn.className = 'play';
      this.video.pause()
    }
  }

  toggleVolumeUpMute($event: MouseEvent) {
    if (this.video.volume === 0) {
      this.volumeUpMuteBtn.className = 'up';
      this.video.volume = 1
    }
    else {
      this.volumeUpMuteBtn.className = 'mute';
      this.video.volume = 0
    }
  }

  toggleFullScreen($event: MouseEvent) {
    if (this.onOffFullScreenBtn.className === 'off') {
      this.onFullScreen(this.videoFrame)
      this.onOffFullScreenBtn.className = 'on';
    }
    else {
      this.offFullScreen(this.videoFrame)
      this.onOffFullScreenBtn.className = 'off';
    }
  }

  onFullScreen(element) {
    if (element.requestFullscreen) {
      element.requestFullscreen()
        .catch(err => {
          alert(`Error attempting to enable full-screen mode: ${err.message} (${err.name})`);
        });
    } else if (element.msRequestFullscreen) {
      element.msRequestFullscreen();
    } else if (element.mozRequestFullScreen) {
      element.mozRequestFullScreen();
    } else if (element.webkitRequestFullscreen) {
      element.webkitRequestFullscreen();
    }
  }

  offFullScreen(element) {
    if (document.exitFullscreen) {
      document.exitFullscreen()
        .then(() => console.log('Document Exited from Full screen mode'))
        .catch((err) => console.error(err));
    } else if (element.msExitFullscreen) {
      element.msExitFullscreen();
    } else if (element.mozCancelFullScreen) {
      element.mozCancelFullScreen();
    } else if (element.webkitExitFullscreen) {
      element.webkitExitFullscreen();
    }
  }

  timeupdateListener(ev) {
    const barPos = this.video.currentTime / this.video.duration;
    this.playbackBar.style.width = barPos * 100 + '%';
    this.currentTime = this.formatSeconds(this.video.currentTime)
    if (this.video.ended) {
      this.playPauseBtn.className = 'play';
    }
  }

  loadedMetaDataListener(ev) {
    const totalSec = this.video.duration;
    this.totalTime = this.formatSeconds(totalSec);
  }

  formatSeconds(secs: number): string {
    let hours: any = Math.floor(secs / (60 * 60))

    const divisorForMinutes = secs % (60 * 60)
    let minutes: any = Math.floor(divisorForMinutes / 60)

    const divisorForSeconds = divisorForMinutes % (60)
    let seconds: any = Math.ceil(divisorForSeconds)

    if (seconds === 60) {
      seconds = 0;
      minutes = minutes + 1
      if (minutes === 60) {
        minutes = 0;
        hours = hours + 1
      }
    }

    hours = this.intToString(hours);
    minutes = this.intToString(minutes);
    seconds = this.intToString(seconds);

    return hours + ':' + minutes + ':' + seconds;
  }

  intToString(time) {
    return time < 10 ? ('0' + time) : time
  }
  // end: player functions

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

  openChat () {
    document.getElementById('chatForm').style.display = 'block';
    document.getElementById('showChat').style.display = 'none';
  }

  closeChat() {
      document.getElementById('chatForm').style.display = 'none';
      document.getElementById('showChat').style.display = 'block';

  }
}
