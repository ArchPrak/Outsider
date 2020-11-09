import {Component, Inject} from '@angular/core';
import {MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';
import { HttpClient } from '@angular/common/http';
import {MatTableModule} from '@angular/material/table';

@Component({
  selector: 'display_reg',
  templateUrl: 'display_reg.component.html',
  styleUrls: ['display_reg.component.css']
})

export class DisplayRegistrationTable {
  serverData: object;
  displayedColumns: object;
  rows: Array<object>;
  rid: Array<number>;
  sid: Array<number>;
  sname: Array<string>;
  team_mates: Array<Array<string>>;
  constructor(public dialogRef: MatDialogRef<DisplayRegistrationTable>, private httpClient: HttpClient, @Inject(MAT_DIALOG_DATA) public data2: any) {
    this.displayedColumns = ['registration_id', 'student_id', 'student_name', 'student_names', 'prize'];
  }

  ngOnInit() {

    this.httpClient.post('http://127.0.0.1:5000/show_reg', {'e_id': this.data2.event[0]}).toPromise().then(data => {
        this.serverData = data as JSON;
        console.log(this.serverData["data"]);
        this.rows = this.serverData["data"]
    });
  }

  onClick() {
    this.dialogRef.close();
  }

}

