import { Settings as LayoutSettings } from '@ant-design/pro-layout';

const Settings: LayoutSettings & {
  pwa?: boolean;
  logo?: string;
} = {
  "navTheme": "light",
  "layout": "top",
  "contentWidth": "Fixed",
  "fixedHeader": false,
  "fixSiderbar": true,
  "pwa": false,
  "logo": "/logo.png",
  "headerHeight": 48,
  "splitMenus": false,
  "footerRender": false,
  "menuRender": false
};

export default Settings;

