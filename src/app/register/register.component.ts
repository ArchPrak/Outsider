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
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css', '../../../node_modules/materialize-css/dist/css/materialize.min.css', '../../../node_modules/bootstrap/dist/css/bootstrap.min.css']
})


export class RegisterComponent {
  infoForm: FormGroup;
  serverData: JSON;
  show: number;
  message: string;
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
    if(this.infoForm.value['first_name'] && this.infoForm.value['last_name'] && this.infoForm.value['password'] && this.infoForm.value['email'] && this.infoForm.value['phone_no'] ) {
        this.httpClient.post('http://127.0.0.1:5000/newuser', {'first_name': this.infoForm.value['first_name'], 'last_name': this.infoForm.value['last_name'], 'email': this.infoForm.value["email"], 'password': this.infoForm.value["password"], 'phone_no': this.infoForm.value['phone_no']} ).subscribe(data => {

        this.serverData = data as JSON;
        console.log(this.serverData);
        if(this.serverData["result"] == "successful") {
          this.message = "Successful!"
          this.show = 1;
          //this.router.navigate(['/login']);
        }
        else {
          this.message = "That email address already belongs to another account!"
          this.show = 0;
        }
      });
    }
    else {
      this.message = "Enter all the details!"
      this.show = 0;
    }
  }

  messdis() {
    if(this.message == "That email address already belongs to another account!") {
      this.message = "";
      this.show = 0;
    }
  }
}
