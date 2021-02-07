import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { environment } from '@environments/environment';
import { Room } from '@app/_models';

@Injectable({ providedIn: 'root' })
export class RoomService {
    roomName: string;

    constructor(private http: HttpClient) { }

    generateNewRoom(username: string) {
        return this.http.post<any>(`${environment.apiUrl}/generateNewRoom`, {username})
    }
}
