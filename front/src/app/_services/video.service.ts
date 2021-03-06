import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { environment } from '@environments/environment';

@Injectable({ providedIn: 'root' })
export class VideoService {
    constructor(private http: HttpClient) { }

    getVideo() {
        return this.http.get<any>(`${environment.apiUrl}/getVideoName`);
    }

  streamVideo(videoName: any) {
      return this.http.get<Blob>(`${environment.apiUrl}/uploads/${videoName}`, { observe: 'response', responseType: 'blob' as 'json' });
    }
}
