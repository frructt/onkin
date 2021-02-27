import { Routes, RouterModule } from '@angular/router';

import { HomeComponent } from './home';
import { LoginComponent } from './login';
import { AppComponent } from '@app/app.component';
import { AuthGuard } from './_helpers';
import { MockedComponent } from './mocked';
import { PlayerComponent } from '@app/player';
import { FillRoomComponent } from '@app/fillRoom';

const routes: Routes = [
    { path: '', component: HomeComponent },
    { path: 'login', component: LoginComponent },
    { path: 'mocked', component: MockedComponent, canActivate: [AuthGuard]},
    { path: 'player', component: PlayerComponent, canActivate: [AuthGuard]},
    { path: 'fillRoom', component: FillRoomComponent, canActivate: [AuthGuard]},

    // otherwise redirect to home
    { path: '**', redirectTo: '' }
];

export const appRoutingModule = RouterModule.forRoot(routes);
