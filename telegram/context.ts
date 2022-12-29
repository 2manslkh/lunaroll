import { Context, Scenes } from "telegraf";

// export interface LunarollSession extends Scenes.SceneSessionData {
//   // will be available under `ctx.LunarollSessionProp`
//   tokenAddress: string;
//   withdrawAddress: string;
//   amount: string;
// }

interface LunarollWizardSession extends Scenes.WizardSessionData {
  // will be available under `ctx.scene.session.myWizardSessionProp`
  tokenAddress: string;
  withdrawAddress: string;
  amount: string;
}

export type LunarollContext = Scenes.WizardContext<LunarollWizardSession>;
// export interface LunarollContext extends Context {
//   // will be available under `ctx.myContextProp`
//   tokenAddress: string;
//   withdrawAddress: string;
//   amount: string;
//   // declare scene type
//   scene: Scenes.SceneContextScene<LunarollContext>;
// }
