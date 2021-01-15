import {Component, OnChanges, OnDestroy, OnInit, SimpleChanges} from '@angular/core';
import {AuthenticationService, SocketioService, VideoService} from '@app/_services';
import {HttpResponse} from '@angular/common/http';
import {NgForm} from '@angular/forms'
import {User} from '@app/_models';


@Component({
  selector: 'app-vdo-player',
  templateUrl: './player.component.html',
  styleUrls: ['./player.component.scss']
})

export class PlayerComponent implements OnInit, OnChanges, OnDestroy {

  // socket: SocketioService;
  currentUser: string;
  anotherUser: string;
  videoName: string;
  videoItem;
  data;
  video;
  // video = document.createElement('video');
  isPlaying: boolean;
  message: string;


  constructor(private videoService: VideoService,
              private authenticationService: AuthenticationService,
              private socket: SocketioService) {
    socket.connect();
    this.currentUser = this.authenticationService.currentUserValue.username;
    this.anotherUser = this.authenticationService.currentUserValue.username;
    this.isPlaying = false;
  }

  ngOnInit() {
    this.videoService.getVideo().subscribe(p => {
      this.videoName = p;
    });
    this.videoService.streamVideo('long_video1.mp4').subscribe(
      (response: HttpResponse<Blob>) => {
        this.videoItem = {
          name: 'Video one',
          src: response.url,
          type: 'video/mp4'
        };
        console.log('this.videoItem.src')
      },
      error => console.log('oops!!!', error)
    );
    this.video = document.getElementById('videoId');
    this.onPauseEvent();
    this.onPlayEvent();
    this.changeVideoPositionEvent();
    this.BroadcastMessages()
  }

  ngOnChanges(changes: SimpleChanges) {
    // this.SendMessage()
    // listen chat messages
    // this.BroadcastMessages()
  }

  ngOnDestroy() {}

  BroadcastMessages() {
    this.socket.socketInstance.on('message', (data: string) => {
     if (data) {
      const p = document.createElement('p');
      const spanUsername = document.createElement('span')
      const spanTimestamp = document.createElement('span')
      const br = document.createElement('br');
      if (data['username']) {
          spanUsername.innerHTML = data['username'];
          spanTimestamp.innerHTML = data['time_stamp'];
          p.innerHTML = spanUsername.outerHTML + br.outerHTML + data['msg'] + br.outerHTML + spanTimestamp.outerHTML;
          document.getElementById('message-list').append(p);
      } else {
          // printSysMsg(data.msg)
      }
      // element.innerHTML = data;
      // element.style.background = 'white';
      // element.style.padding =  '15px 30px';
      // element.style.margin = '10px';
      // document.getElementById('message-list').appendChild(element);
      }
    });
  }

  sendMessage(sendForm: NgForm) {
     this.socket.socketInstance.emit('message', {username: this.currentUser, msg: sendForm.value.message});
     const element = document.createElement('li');
     element.innerHTML = this.message;
     element.style.background = 'white';
     element.style.padding =  '15px 30px';
     element.style.margin = '10px';
     element.style.textAlign = 'right';
     document.getElementById('message-list').appendChild(element);
     this.message = '';
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
      this.isPlaying = true;
      if (this.anotherUser === this.currentUser){
          console.log('video is playing from user ' + this.currentUser);
          this.socket.socketInstance.emit('play-video', {username: this.currentUser});
      } else {
          console.log(' ' + this.anotherUser + ' != ' + this.currentUser);
          this.anotherUser = this.currentUser;
      }
  }

  onPlayEvent() {
    this.socket.socketInstance.on('onplay event', data => {
      this.anotherUser = data.username
      this.playVid();
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
    this.isPlaying = false;
    if (this.anotherUser === this.currentUser){
      if (!this.video.seeking) {  // if seeking don't send pause event to server
        console.log('video is paused by user ' + this.currentUser);
        this.socket.socketInstance.emit('pause-video', {username: this.currentUser});
      }
    } else {
      console.log(' ' + this.anotherUser + ' != ' + this.currentUser);
      this.anotherUser = this.currentUser;
    }
  }

  onPauseEvent() {
    this.socket.socketInstance.on('onpause event', data => {
      this.anotherUser = data.username
      this.pauseVid();
    });
  }

  onSeeked() {
    if (this.anotherUser === this.currentUser){
      console.log(this.video.currentTime);
      this.socket.socketInstance.emit('change-video-position',
        {current_position: this.video.currentTime, username: this.currentUser});
    } else {
      console.log(' ' + this.anotherUser + ' != ' + this.currentUser);
      this.anotherUser = this.currentUser;
    }
  }

  changeVideoPositionEvent() {
    this.socket.socketInstance.on('change video position event', data => {
        console.log('difference in positions (sec): ' + Math.abs((data.current_position - this.video.currentTime)))
        if ((this.video.currentTime !== data.current_position) && data.username !== this.currentUser) {
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
}
