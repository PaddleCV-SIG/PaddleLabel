import component from './fa-IR/component';
import globalHeader from './fa-IR/globalHeader';
import menu from './fa-IR/menu';
import pwa from './fa-IR/pwa';
import settingDrawer from './fa-IR/settingDrawer';
import settings from './fa-IR/settings';

export default {
  'navBar.lang': 'لغة',
  'layout.user.link.help': 'مساعدة',
  'layout.user.link.privacy': 'الإجمالية',
  'layout.user.link.terms': 'مصلحات',
  'app.preview.down.block': 'قم بتنزيل هذه الصفحة إلى مشروع محلي',
  ...globalHeader,
  ...menu,
  ...settingDrawer,
  ...settings,
  ...pwa,
  ...component,
};
