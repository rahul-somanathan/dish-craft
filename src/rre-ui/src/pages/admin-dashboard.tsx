import React from "react";
import {
  AppstoreOutlined,
  MailOutlined,
  SettingOutlined,
} from "@ant-design/icons";
import type { MenuProps } from "antd";
import { Breadcrumb, Layout, Menu, theme } from "antd";
import Typography from "antd/es/typography/Typography";
import Title from "antd/es/typography/Title";

const { Header, Content, Sider } = Layout;

const leftNavMenuItems: MenuProps["items"] = [
  {
    key: "1",
    icon: <MailOutlined />,
    label: "Dashboard",
    children: [
      { key: "11", label: "Admin Dashboard" },
      { key: "12", label: "Data Dashboard" },
      { key: "13", label: "EDA Dashboard" },
      { key: "14", label: "Model Dashboard" },
    ],
  },
  {
    key: "2",
    icon: <SettingOutlined />,
    label: "Settings",
    children: [
      { key: "21", label: "Profile" },
      { key: "22", label: "Contact Us" },
    ],
  },
];

const App: React.FC = () => {
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();

  return (
    <Layout style={{ minHeight: "100vh" }}>
      <Header style={{ display: "flex", alignItems: "center" }}>
        <div className="demo-logo" />
        <Typography>
          <Title level={5}> DishCraft</Title>
        </Typography>

        {/* <Menu
          theme="dark"
          mode="horizontal"
          defaultSelectedKeys={["2"]}
          items={items1}
          style={{ flex: 1, minWidth: 0 }}
        /> */}
      </Header>
      <Layout>
        <Sider width={200} style={{ background: colorBgContainer }}>
          <Menu
            mode="inline"
            defaultSelectedKeys={["1"]}
            defaultOpenKeys={["sub1"]}
            style={{ height: "100%", borderRight: 0 }}
            items={leftNavMenuItems}
          ></Menu>
        </Sider>
        <Layout style={{ padding: "0 24px 24px" }}>
          <Breadcrumb style={{ margin: "16px 0" }}>
            <Breadcrumb.Item>Home</Breadcrumb.Item>
            <Breadcrumb.Item>List</Breadcrumb.Item>
            <Breadcrumb.Item>App</Breadcrumb.Item>
          </Breadcrumb>
          <Content
            style={{
              padding: 24,
              margin: 0,
              minHeight: 280,
              background: colorBgContainer,
              borderRadius: borderRadiusLG,
            }}
          >
            Content
          </Content>
        </Layout>
      </Layout>
    </Layout>
  );
};

export default App;
