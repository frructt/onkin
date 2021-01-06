import { Component, OnInit } from '@angular/core';
import { VideoService } from '@app/_services';
import {HttpResponse} from '@angular/common/http';


@Component({
  selector: 'app-vdo-player',
  templateUrl: './player.component.html',
  styleUrls: ['./player.component.scss']
})

export class PlayerComponent implements OnInit {

  videoName: string;
  videoItem;
  data;


  constructor(private videoService: VideoService) {
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
      },
      error => console.log('oops!!!', error)
    );
  }

  videoPlayerInit(data) {
    this.data = data;

    this.data.getDefaultMedia().subscriptions.loadedMetadata.subscribe(this.initVdo.bind(this));
  }

  initVdo() {
    this.data.play();
  }
}
