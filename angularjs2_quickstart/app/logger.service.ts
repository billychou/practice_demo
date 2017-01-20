/**
 *
 * Created by songchuanzhou on 17/1/18.
 */

import { Injectable } from '@angular/core';

@Injectable()
export class Logger {
  logs: string[] = [];

  log(message: string) {
    this.logs.push(message);
    console.log(message);
  }
}
