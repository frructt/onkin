import { Component } from '@angular/core';
import {Router} from '@angular/router';

import { AuthenticationService } from './_services';
import { User } from './_models';
import { SocketioService } from './_services';

@Component({ selector: 'app', templateUrl: 'app.component.html' })
export class AppComponent {
    currentUser: User;

    constructor(
        private router: Router,
        private authenticationService: AuthenticationService,
        private socketService: SocketioService
    ) {
        this.socketService.setupSocketConnection();
        this.authenticationService.currentUser.subscribe(x => this.currentUser = x);
    }

    logout() {
        this.authenticationService.logout();
        this.router.navigate(['/login']);
    }
}
