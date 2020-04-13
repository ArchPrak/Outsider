import { Component, OnInit } from '@angular/core'
import { HttpClient } from '@angular/common/http';
import { FormGroup, FormControl, ReactiveFormsModule, EmailValidator } from '@angular/forms';
import { StudentService } from '../student.service';
import { Router, Routes, RouterModule } from '@angular/router';
import { ProfileComponent } from '../profile/profile.component';
import { OrganiserService } from '../organiser.service';

const routes: Routes = [
  {path: 'profile', component: ProfileComponent},
]

@Component({
  selector:'login',
  templateUrl: './login.component.html'
})


export class LoginComponent {

  credentialsForm: FormGroup;
  serverData: JSON;
  message: string;

  constructor(private httpClient: HttpClient, private data: OrganiserService, private data1: StudentService, public router: Router) {
    this.credentialsForm = new FormGroup({
      email: new FormControl(''),
      password: new FormControl(''),
      account_type: new FormControl('')
    });
  }

  checkCred(account) {
      console.log(account);
      this.httpClient.post('http://127.0.0.1:5000/checkuser', {'email': this.credentialsForm.value["email"], 'password': this.credentialsForm.value["password"] , 'account_type': account}).subscribe(data => {
      this.serverData = data as JSON;
      console.log(this.serverData);
      if('first_name' in this.serverData && account == "organiser" ) {
        this.data.changeMessage(this.serverData);
        console.log('here');
        this.router.navigate(['/profile']);
      }
      else if('first_name' in this.serverData && account == "student" ) {
        this.data1.changeMessage(this.serverData);
        this.router.navigate(['/shome'])
      }
    })
  }
}
