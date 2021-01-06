import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { environment } from '@environments/environment';
import { Video } from '@app/_models';

@Injectable({ providedIn: 'root' })
export class VideoService {
    constructor(private http: HttpClient) { }

    getVideo() {
        return this.http.get<string>(`${environment.apiUrl}/getVideoName`);
    }

  streamVideo(videoName: string) {
      return this.http.get<Blob>(`${environment.apiUrl}/uploads/${videoName}`, { observe: 'response', responseType: 'blob' as 'json' });
    }
}
