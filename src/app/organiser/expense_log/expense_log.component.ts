import {Component, Inject} from '@angular/core';
import {MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'expense-log',
  templateUrl: 'expense_log.component.html',
  styleUrls: ['expense_log.component.css']
})

export class ExpenseLog {
  serverData: object;
  displayedColumns: object;
  rows: Array<object>;
  data: Array<string>;
  amount: Array<number>;
  constructor(public dialogRef: MatDialogRef<ExpenseLog>, private httpClient: HttpClient, @Inject(MAT_DIALOG_DATA) public data2: any) {
    this.displayedColumns = ['reason', 'amount'];
  }

  ngOnInit() {

    this.httpClient.post('http://127.0.0.1:5000/event_log', {'e_id': this.data2.event[0]}).toPromise().then(data => {
        this.serverData = data as JSON;
        console.log(this.serverData["data"]);
        var data1 = []
        var amount1 = []
        for(var x in this.serverData["data"]) {
          console.log(this.serverData["data"][x][3] + this.serverData["data"][x][2]);
          data1.push(this.serverData["data"][x][3]);
          amount1.push(this.serverData["data"][x][2]);
        }
        this.data = data1;
        this.amount = amount1;
        this.random();
    });
  }

  random() {
    console.log(this.data);
    console.log(this.amount);
    this.rows = [];
    for(var x = 0; x < this.data.length; x++) {
      this.rows.push({});
      this.rows[x] = ({"data": this.data[x], "amount":this.amount[x]});
    }
  }

  onClick() {
    this.dialogRef.close();
  }

}
