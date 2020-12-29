import {Component, OnInit} from '@angular/core';
import {AuthenticationService, UserService} from '@app/_services';
import {Router} from '@angular/router';

@Component({ templateUrl: 'home.component.html' ,
             styleUrls: ['home.component.scss']
})
export class HomeComponent implements OnInit {
    submitted = false;

    constructor(private userService: UserService,
                private authenticationService: AuthenticationService,
                private router: Router) { }

    ngOnInit() {
    }

    onCreateRoomSubmit() {
      this.submitted = true;

      const currentUser = this.authenticationService.currentUserValue;
      if (currentUser) {
          this.router.navigate(['/mocked']);
          return true;
      }

      // not logged in so redirect to login page
      this.router.navigate(['/login'], { queryParams: { returnUrl: '/mocked' } });
      return false;
    }

    onWatchVideoSubmit() {
      this.submitted = true;

      const currentUser = this.authenticationService.currentUserValue;
      if (currentUser) {
        this.router.navigate(['/mocked']);
        return true;
      }

      // not logged in so redirect to login page
      this.router.navigate(['/login'], { queryParams: { returnUrl: '/mocked' } });
      return false;
    }
}
