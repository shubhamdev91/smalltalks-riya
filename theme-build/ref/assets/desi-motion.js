/* A finite, deterministic clock. DOM geometry and asset loading live in desi.js. */
(function(root){
 class DesiMotion {
  constructor({count=7,index=0,autoplay=true,reduced=false}={}){this.count=count;this.index=index;this.tone=1;this.elapsed=0;this.visited=1;this.mode=autoplay?'auto':'manual';this.reasons=new Set(reduced?['reduced']:[]);this.phase='signature';this.destroyed=false;}
  get running(){return !this.destroyed&&this.mode==='auto'&&this.reasons.size===0;}
  pause(reason,on=true){on?this.reasons.add(reason):this.reasons.delete(reason);}
  resume(){this.mode='auto';this.visited=1;this.elapsed=0;this.phase='signature';this.reasons.delete('user');this.reasons.delete('manual');this.reasons.delete('assets');}
  next(){this.mode='manual';this.reasons.delete('user');this.index=(this.index+1)%this.count;this.elapsed=0;this.phase='signature';}
  tick(delta){if(!this.running)return;this.elapsed+=Math.max(0,Math.min(delta,100));
   if(this.elapsed>=4000){this.elapsed-=4000;this.index=(this.index+1)%this.count;this.visited++;}
   if(this.visited>=3&&this.elapsed>=3300){this.elapsed=3300;this.mode='held';this.phase='signature';return;}
   this.phase=this.elapsed<1600?'signature':this.elapsed<1900?'accent-flight':this.elapsed<2350?'accent':this.elapsed<2650?'return-flight':this.elapsed<3300?'signature':this.elapsed<3900?'next-flight':'commit';
  }
 }
 root.DesiMotion=DesiMotion;
})(typeof window==='undefined'?globalThis:window);
