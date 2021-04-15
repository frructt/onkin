import {Component, OnInit} from '@angular/core';
import {AuthenticationService, UserService, SocketioService, RoomService} from '@app/_services';
import {Router} from '@angular/router';
import { io } from 'socket.io-client';
import {environment} from '@environments/environment';

@Component({ templateUrl: 'home.component.html' ,
             styleUrls: ['home.component.scss']
})
export class HomeComponent implements OnInit {
    submitted = false;

    constructor(private userService: UserService,
                private authenticationService: AuthenticationService,
                private router: Router,
                private roomService: RoomService,
                private socket: SocketioService) { }

    ngOnInit() {
      // this.socket.connect();
      // this.sendmessage();
      // this.socket.iniServerSocket()
    }

    // sendmessage() {
    //   this.socket.socketInstance.emit('new-message', 'Hi-flask');
    // }

    onCreateRoomSubmit() {
      this.submitted = true;

      const currentUser = this.authenticationService.currentUserValue;
      if (currentUser) {
          this.router.navigate(['/player']);
          return true;
      }

      // not logged in so redirect to login page
      this.router.navigate(['/login'], { queryParams: { returnUrl: '/player' } });
      return false;
    }

    onWatchVideoSubmit() {
      this.submitted = true;

      const currentUser = this.authenticationService.currentUserValue;
      if (currentUser) {
        this.router.navigate(['/fillRoom']);
        return true;
      }

      // not logged in so redirect to login page
      this.router.navigate(['/login'], { queryParams: { returnUrl: '/fillRoom' } });
      return false;
    }
}
