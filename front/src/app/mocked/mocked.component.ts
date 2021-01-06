import { Component } from '@angular/core';
import { first } from 'rxjs/operators';

import { User } from '@app/_models';
import { UserService } from '@app/_services';

@Component({ templateUrl: 'mocked.component.html' })
export class MockedComponent {
    loading = false;
    users: User[];

    constructor(private userService: UserService) { }

    ngOnInit() {
        this.loading = true;
        this.userService.getAllUsers().pipe(first()).subscribe(users => {
            this.loading = false;
            this.users = users;
        });
    }
}
