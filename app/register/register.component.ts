import { Component } from '@angular/core'
import { HttpClient } from '@angular/common/http';
import { FormGroup, FormControl, ReactiveFormsModule, EmailValidator } from '@angular/forms';

import { Router, Routes, RouterModule } from '@angular/router';
import { ProfileComponent } from '../profile/profile.component';

const routes: Routes = [
  {path: 'profile', component: ProfileComponent},
]


@Component({
  selector:'register',
  templateUrl: './register.component.html'
})


export class RegisterComponent {
  infoForm: FormGroup;
  serverData: JSON;

  constructor(private httpClient: HttpClient, public router: Router) {
    this.infoForm = new FormGroup({
      first_name: new FormControl(''),
      last_name: new FormControl(''),
      email: new FormControl(''),
      password: new FormControl(''),
      phone_no: new FormControl(''),
    });
  }

  newUser() {
    var reqData = {'first_name': this.infoForm.value['first_name'], 'last_name': this.infoForm.value['last_name'], 'email': this.infoForm.value["email"], 'password': this.infoForm.value["password"], 'phone_no': this.infoForm.value['phone_no']};
    if(reqData["first_name"].length != 0 && reqData["last_name"].length != 0 && reqData["email"].length != 0 && reqData["password"].length != 0 && reqData["phone_no"].length != 0) {
      this.httpClient.post('http://127.0.0.1:5000/newuser', reqData ).subscribe(data => {
      this.serverData = data as JSON;
      console.log(this.serverData);
      this.router.navigate(['/profile']);
      })
    }
  }
}
