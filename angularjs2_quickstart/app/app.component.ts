import { Component } from '@angular/core';

@Component({
  //组件中注册选择器、模板、提供商
  selector: 'my-app',
  templateUrl: 'a.html'
})


export class AppComponent  {
  name = 'Angular';
  title = '浏览英雄';
  heroes = ["A","B","C","D"]
  myHero = 'E';
  my_favourite_hero = this.heroes[0];
}
