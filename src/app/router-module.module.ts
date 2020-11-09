import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Routes, RouterModule } from '@angular/router';

import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { ProfileComponent } from './profile/profile.component';
import { CreateEvent } from './organiser/create_event/create_event.component';
import { AllEvents } from './organiser/list_event/list_event.component';
import { OrganiserStatistics } from './organiser/organiser_statistics/organiser_statistics.component';
import { ShomeComponent } from './shome/shome.component';
import { DispEvents } from './student/list_event/list_event.component';
import { RegEvent } from './student/reg_event/reg_event.component';
import { GetTeam } from './student/get_team/get_team.component';
import { DispPrizes } from './student/list_prize/list_prize.component';
import { EventDet } from './student/event_details/event_details.component';
import { DispOrg } from './student/display_org/display_org.component';
import { TeamInput } from './student/team_input/team_input.component';
import { AfterReg } from './student/after_reg/after_reg.component';
import {AddHobby} from './student/add_hobby/add_hobby.component';

const appRoutes: Routes = [
  {path: 'login', component: LoginComponent},
  {path: 'register', component: RegisterComponent},
  {path: 'profile', component: ProfileComponent},
  {path: 'newevent', component: CreateEvent},
  {path: 'allevents', component: AllEvents},
  {path: 'statistics', component: OrganiserStatistics},
  {path: 'studentprofile', component: ShomeComponent},
  {path: 'dispevents', component: DispEvents},
  {path: 'regevent', component: RegEvent},
  {path:'getteam',component: GetTeam},
  {path: 'dispprizes', component: DispPrizes},
  {path:'eventdet',component: EventDet},
  {path:'disporg',component: DispOrg},
  {path:'teaminp',component: TeamInput},
  {path:'afterreg',component: AfterReg},
  {path: 'eventdet', component: EventDet},
  {path: 'addhobby', component: AddHobby},

]

@NgModule({
    imports: [
        RouterModule.forRoot(appRoutes)
    ],
    exports: [
        RouterModule
    ]
})
export class AppRoutingModule {}
