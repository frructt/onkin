import { Injectable } from '@angular/core';
// import * as Talk from 'talkjs'
import { User} from '@app/_models';
import { AuthenticationService } from '@app/_services';

@Injectable({
  providedIn: 'root'
})
export class TalkService {
  private static APP_ID = 'YOUR_APP_ID';
   private currentTalkUser: User['username'];
   // private currentSessionDeferred = new Deferred();

   constructor(private authenticationService: AuthenticationService) { }

   // async createCurrentSession() {
   //    await Talk.ready;
   //
   //    const currentUser = await this.authenticationService.getCurrentUser();
   //    const currentTalkUser = await this.createTalkUser(currentUser);
   //    const session = new Talk.Session({
   //       appId: TalkService.APP_ID,
   //       me: currentTalkUser
   //    });
   //    this.currentTalkUser = currentTalkUser;
   //    this.currentSessionDeferred.resolve(session);
   // }

   // async createTalkUser(applicationUser: User) : Promise {
   // await Talk.ready;
   //
   // return new Talk.User({
   //    id: applicationUser.id,
   //    name: applicationUser.username,
   //    photoUrl: applicationUser.profilePictureUrl
   //    });
   // }
}
