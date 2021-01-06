import { Component, OnInit } from '@angular/core';
import { VideoService } from '@app/_services';
import {first} from 'rxjs/operators';
import { Observable, EMPTY, throwError, of } from 'rxjs';
import { catchError } from 'rxjs/operators';
import base64url from 'base64url';
import {flatMap} from 'rxjs/internal/operators';
import {HttpResponse} from '@angular/common/http';
import {DomSanitizer} from '@angular/platform-browser';


@Component({
  selector: 'app-vdo-player',
  templateUrl: './player.component.html',
  styleUrls: ['./player.component.scss']
})

export class PlayerComponent implements OnInit {

  videoName: string;
  streamVideo;
  streamVideoURL;

  constructor(private videoService: VideoService, private sanitizer: DomSanitizer) {
  }

  ngOnInit() {
    this.videoService.getVideo().subscribe(p => {
      this.videoName = p;
    });
    this.videoService.streamVideo('long_video1.mp4').subscribe(
      (response: HttpResponse<Blob>) => {
        this.streamVideoURL = response.url;
        // const binaryData = [];
        // binaryData.push(response.body);
        // this.streamVideoURL = URL.createObjectURL(new Blob(binaryData, { type: 'blob' }));
        // this.sanitizer.bypassSecurityTrustResourceUrl(this.streamVideoURL);

        // const cuttedPart = this.streamVideoURL.split('/');
        // const decodedCuttedPart = atob(cuttedPart[3]);
        // this.streamVideoURL = cuttedPart[0] + cuttedPart[1] + cuttedPart[2] + decodedCuttedPart;

        // .streamVideoURL = base64url.decode(this.streamVideoURL)
      },
      error => console.log('oops!!!', error)
    );
  }

  OnDestroy() {
    URL.revokeObjectURL(this.streamVideoURL)
  }


}
