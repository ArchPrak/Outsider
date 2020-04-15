import {Component, Inject} from '@angular/core';
import {MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';
import { HttpClient } from '@angular/common/http';
import {MatTableModule} from '@angular/material/table';

import { Router, Routes, RouterModule } from '@angular/router';
import { StudentService } from '../../student.service';
import { ArrayDataSource } from '@angular/cdk/collections';
@Component({
  selector: 'display_reg',
  templateUrl: 'display_org.component.html',

})

export class DispOrg {
  orgData: object;
  noOrg : String;
  message:object;
  rid: Array<number>;
  sid: Array<number>;
  sname: Array<string>;
  team_mates: Array<Array<string>>;
  constructor(public dialogRef: MatDialogRef<DispOrg>, private httpClient: HttpClient,private data: StudentService, public router: Router, @Inject(MAT_DIALOG_DATA) public data2: any) {
   //this.displayedColumns = [first_name','last_name','email'];
  }

  ngOnInit() {
    this.data.currentMessage.subscribe((message) => this.message = message);
    if(Object.keys(this.message).length == 0) {
      this.router.navigateByUrl('/login');
    }
    this.httpClient.post('http://127.0.0.1:5000/student/orgdet', {'o_id':this.message['o_id']}).subscribe(data => {
          this.orgData= data as JSON;
          console.log("Organiser")
          console.log(this.orgData);
          this.noOrg="";
          if (Object.keys(this.orgData).length == 0){
            console.log("No data");
           document.getElementById("orgn").innerHTML="Unavailable! Sorry.";
          }
        });

  }

  onClick() {
    this.dialogRef.close();
  }

}
