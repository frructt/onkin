import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { environment } from '@environments/environment';
import { Room } from '@app/_models';
import {map} from 'rxjs/operators';
import {AuthenticationService} from '@app/_services/authentication.service';

@Injectable({ providedIn: 'root' })
export class RoomService {
    roomId: string;

    constructor(private http: HttpClient,
                private authenticationService: AuthenticationService) { }

    generateNewRoom(username: string) {
        return this.http.post<any>(`${environment.apiUrl}/generateNewRoom`, {username})
    }

    fillRoom(roomId: string, username: string) {
        return this.http.post<any>(`${environment.apiUrl}/fillRoom`, { roomId, username })
            .pipe(map(response => {
                  // add room credentials in local storage to keep user added in current room
                  this.authenticationService.currentUserValue.roomId = roomId
                  localStorage.setItem('currentUser', JSON.stringify(this.authenticationService.currentUserValue));
                  return response.result;
            }));
    }
}
