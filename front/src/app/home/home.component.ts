import { Component } from '@angular/core';
import { first } from 'rxjs/operators';

import { User } from '@app/_models';
import { UserService } from '@app/_services';

@Component({ templateUrl: 'home.component.html' })
export class HomeComponent {
    loading = false;
    users: User[];

    constructor(private userService: UserService) { }

  // tslint:disable-next-line:use-lifecycle-interface
    ngOnInit() {
        this.loading = true;
        this.userService.getAllUsers().pipe(first()).subscribe(users => {
            this.loading = false;
            this.users = users;
        });
    }
}
