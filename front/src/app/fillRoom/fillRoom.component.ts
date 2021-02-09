import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { first } from 'rxjs/operators';

import { AuthenticationService, RoomService } from '@app/_services';

@Component({ templateUrl: 'fillRoom.component.html' ,
             styleUrls: ['fillRoom.component.scss']
})
export class FillRoomComponent implements OnInit {
    fillRoomForm: FormGroup;
    loading = false;
    submitted = false;
    error = '';

    constructor(
        private formBuilder: FormBuilder,
        private route: ActivatedRoute,
        private router: Router,
        private authenticationService: AuthenticationService,
        private roomService: RoomService
    ) {}

    ngOnInit() {
        this.fillRoomForm = this.formBuilder.group({
            roomId: ['', Validators.required]
        });
    }

    // convenience getter for easy access to form fields
    get f() { return this.fillRoomForm.controls; }

    onSubmit() {
        this.submitted = true;

        // stop here if form is invalid
        if (this.fillRoomForm.invalid) {
            return;
        }

        this.loading = true;
        this.roomService.fillRoom(this.f.roomId.value, this.authenticationService.currentUserValue.username)
            .pipe(first())
            .subscribe(
                data => {
                    this.router.navigate(['/player']);
                },
                error => {
                    this.error = error;
                    this.loading = false;
                });
    }
}
