
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;
import javax.swing.JOptionPane;
import javax.swing.table.DefaultTableModel;
import javax.swing.table.TableModel;

/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author uttka
 */
public class frmVolACt extends javax.swing.JPanel {

    
    public frmVolACt() {
        initComponents();
        displayDataAct();
        displayDataVol();
        displayDataVolAct();
    }
    private void displayDataVolAct()
    {
        jTextField1.setText(" ");
        jTextField2.setText(" ");
        
        jTable3.setModel(new DefaultTableModel(null,new String[]{"Volunteer ID", "Activity ID", "Volunteer Name", "Activity"}));
        try {
            Connection conn = DriverManager.getConnection("jdbc:postgresql://localhost:5433/diatech1", "postgres","QWERTY@1738");
            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery("Select * from tblvolact");
            while (rs.next()) {
                String volID = rs.getString("volid");
                String volunteer = rs.getString("volname");
                String actID = rs.getString("actid");
                String activity = rs.getString("actname");
            
                              
            // Array to hold the values for table display
            String[] tbvolact = {volID, actID, volunteer, activity};  
            // Displaying data into table
            
            DefaultTableModel tblModel = (DefaultTableModel)jTable3.getModel();
            tblModel.addRow(tbvolact);
           // jTable1.getColumnModel().getColumn(3).setMaxWidth(0);
           }
           rs.close();
         
           
            
        } catch (Exception e) {
            JOptionPane.showMessageDialog(null, "Cannot connect to the database. Please Setup the database and try again ");
            //System.out.println(e.getMessage());
        }}
    private void displayDataAct()
    {
        jTextField1.setText(" ");
        jTextField2.setText(" ");
        
        jTable1.setModel(new DefaultTableModel(null,new String[]{"Activity ID", "Activity"}));
        try {
            Connection conn = DriverManager.getConnection("jdbc:postgresql://localhost:5433/diatech1", "postgres","QWERTY@1738");
            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery("Select * from tblactivity");
            while (rs.next()) {
                String actID = rs.getString("actid");
                String activity = rs.getString("actname");
            
                              
            // Array to hold the values for table display
            String[] tbact = {actID, activity};  
            // Displaying data into table
            
            DefaultTableModel tblModel = (DefaultTableModel)jTable1.getModel();
            tblModel.addRow(tbact);
           // jTable1.getColumnModel().getColumn(3).setMaxWidth(0);
           }
           rs.close();
         
           
            
        } catch (Exception e) {
            JOptionPane.showMessageDialog(null, "Cannot connect to the database. Please Setup the database and try again ");
            //System.out.println(e.getMessage());
        }}
    private void displayDataVol()
    {
        jTextField1.setText(" ");
        jTextField2.setText(" ");
        
        jTable2.setModel(new DefaultTableModel(null,new String[]{"Volunteer ID", "Volunteer Name"}));
        try {
            Connection conn = DriverManager.getConnection("jdbc:postgresql://localhost:5433/diatech1", "postgres","QWERTY@1738");
            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery("Select * from tblvolunteer");
            while (rs.next()) {
                String volID = rs.getString("volid");
                String volunteer = rs.getString("volname");
            
                              
            // Array to hold the values for table display
            String[] tbvol = {volID, volunteer};  
            // Displaying data into table
            
            DefaultTableModel tblModel = (DefaultTableModel)jTable2.getModel();
            tblModel.addRow(tbvol);
           // jTable1.getColumnModel().getColumn(3).setMaxWidth(0);
           }
           rs.close();
         
           
            
        } catch (Exception e) {
            JOptionPane.showMessageDialog(null, "Cannot connect to the database. Please Setup the database and try again ");
            //System.out.println(e.getMessage());
        }}
    private void getSelectedRowAct(){
      int i = jTable1.getSelectedRow(); 
      TableModel tm = jTable1.getModel();
      jComboBox1.removeAllItems();
      jComboBox1.addItem(tm.getValueAt(i, 0).toString()); 
      jComboBox1.setSelectedIndex(0);
      jTextField1.setText(tm.getValueAt(i, 1).toString());
      // as we have teh values in the combobox, this switch will check and set the required index
      
  }
    private void getSelectedRowVol(){
      int i = jTable2.getSelectedRow(); 
      TableModel tm = jTable2.getModel();
      jComboBox2.removeAllItems();
      jComboBox2.addItem(tm.getValueAt(i, 0).toString()); 
      jComboBox2.setSelectedIndex(0);
      jTextField2.setText(tm.getValueAt(i, 1).toString());
      // as we have teh values in the combobox, this switch will check and set the required index
      
  }
    private void getSelectedRowVolAct(){
      int i = jTable3.getSelectedRow(); 
      TableModel tm = jTable3.getModel();
      jComboBox1.removeAllItems();
      jComboBox1.addItem(tm.getValueAt(i, 1).toString()); 
      jComboBox1.setSelectedIndex(0);
      jComboBox2.removeAllItems();
      jComboBox2.addItem(tm.getValueAt(i, 0).toString()); 
      jComboBox2.setSelectedIndex(0);
      jTextField2.setText(tm.getValueAt(i, 2).toString());
      jTextField1.setText(tm.getValueAt(i, 3).toString());
      
  }
    /**
     * This method is called from within the constructor to initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is always
     * regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        jLabel1 = new javax.swing.JLabel();
        jScrollPane1 = new javax.swing.JScrollPane();
        jTable1 = new javax.swing.JTable();
        jScrollPane2 = new javax.swing.JScrollPane();
        jTable2 = new javax.swing.JTable();
        jLabel2 = new javax.swing.JLabel();
        jLabel3 = new javax.swing.JLabel();
        jButton1 = new javax.swing.JButton();
        jTextField1 = new javax.swing.JTextField();
        jTextField2 = new javax.swing.JTextField();
        jScrollPane3 = new javax.swing.JScrollPane();
        jTable3 = new javax.swing.JTable();
        jComboBox1 = new javax.swing.JComboBox<>();
        jComboBox2 = new javax.swing.JComboBox<>();
        jButton2 = new javax.swing.JButton();
        jButton4 = new javax.swing.JButton();
        jButton5 = new javax.swing.JButton();

        jLabel1.setFont(new java.awt.Font("Tahoma", 1, 24)); // NOI18N
        jLabel1.setText("Add Volunteer to Activities");

        jTable1.setModel(new javax.swing.table.DefaultTableModel(
            new Object [][] {

            },
            new String [] {
                "Activity ID", "Activity "
            }
        ) {
            Class[] types = new Class [] {
                java.lang.String.class, java.lang.String.class
            };

            public Class getColumnClass(int columnIndex) {
                return types [columnIndex];
            }
        });
        jTable1.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseClicked(java.awt.event.MouseEvent evt) {
                jTable1MouseClicked(evt);
            }
        });
        jScrollPane1.setViewportView(jTable1);

        jTable2.setModel(new javax.swing.table.DefaultTableModel(
            new Object [][] {

            },
            new String [] {
                "Volunteer ID", "Volunteer Name"
            }
        ) {
            Class[] types = new Class [] {
                java.lang.String.class, java.lang.String.class
            };

            public Class getColumnClass(int columnIndex) {
                return types [columnIndex];
            }
        });
        jTable2.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseClicked(java.awt.event.MouseEvent evt) {
                jTable2MouseClicked(evt);
            }
        });
        jScrollPane2.setViewportView(jTable2);

        jLabel2.setFont(new java.awt.Font("Tahoma", 1, 13)); // NOI18N
        jLabel2.setText("Activity");

        jLabel3.setFont(new java.awt.Font("Tahoma", 1, 13)); // NOI18N
        jLabel3.setText("Volunteer");

        jButton1.setFont(new java.awt.Font("Tahoma", 1, 13)); // NOI18N
        jButton1.setText("ADD");
        jButton1.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jButton1ActionPerformed(evt);
            }
        });

        jTable3.setModel(new javax.swing.table.DefaultTableModel(
            new Object [][] {

            },
            new String [] {
                "Volunteer ID", "Activity ID", "Volunteer Name", "Activity"
            }
        ) {
            Class[] types = new Class [] {
                java.lang.String.class, java.lang.String.class, java.lang.String.class, java.lang.String.class
            };

            public Class getColumnClass(int columnIndex) {
                return types [columnIndex];
            }
        });
        jTable3.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseClicked(java.awt.event.MouseEvent evt) {
                jTable3MouseClicked(evt);
            }
        });
        jScrollPane3.setViewportView(jTable3);

        jButton2.setText("CLEAR");
        jButton2.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jButton2ActionPerformed(evt);
            }
        });

        jButton4.setText("DELETE");
        jButton4.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jButton4ActionPerformed(evt);
            }
        });

        jButton5.setText("CLOSE");
        jButton5.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jButton5ActionPerformed(evt);
            }
        });

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(this);
        this.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(jScrollPane1, javax.swing.GroupLayout.PREFERRED_SIZE, 195, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(layout.createSequentialGroup()
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addGroup(layout.createSequentialGroup()
                                .addGap(36, 36, 36)
                                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                                    .addComponent(jLabel2)
                                    .addComponent(jLabel3)))
                            .addGroup(layout.createSequentialGroup()
                                .addGap(28, 28, 28)
                                .addComponent(jButton2, javax.swing.GroupLayout.PREFERRED_SIZE, 69, javax.swing.GroupLayout.PREFERRED_SIZE)))
                        .addGap(32, 32, 32)
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addGroup(layout.createSequentialGroup()
                                .addGap(38, 38, 38)
                                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                                    .addComponent(jTextField2, javax.swing.GroupLayout.PREFERRED_SIZE, 133, javax.swing.GroupLayout.PREFERRED_SIZE)
                                    .addComponent(jTextField1, javax.swing.GroupLayout.PREFERRED_SIZE, 133, javax.swing.GroupLayout.PREFERRED_SIZE))
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                                    .addComponent(jComboBox1, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                                    .addComponent(jComboBox2, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)))
                            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                .addComponent(jButton4)
                                .addGap(43, 43, 43)
                                .addComponent(jButton5)))
                        .addGap(18, 18, Short.MAX_VALUE))
                    .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                        .addComponent(jButton1, javax.swing.GroupLayout.PREFERRED_SIZE, 104, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addGap(118, 118, 118)))
                .addComponent(jScrollPane2, javax.swing.GroupLayout.PREFERRED_SIZE, 220, javax.swing.GroupLayout.PREFERRED_SIZE))
            .addGroup(layout.createSequentialGroup()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(layout.createSequentialGroup()
                        .addGap(191, 191, 191)
                        .addComponent(jLabel1))
                    .addGroup(layout.createSequentialGroup()
                        .addGap(50, 50, 50)
                        .addComponent(jScrollPane3, javax.swing.GroupLayout.PREFERRED_SIZE, 646, javax.swing.GroupLayout.PREFERRED_SIZE)))
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addGap(28, 28, 28)
                .addComponent(jLabel1)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING, false)
                    .addGroup(layout.createSequentialGroup()
                        .addGap(53, 53, 53)
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                            .addComponent(jLabel2)
                            .addComponent(jTextField1, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(jComboBox1, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                        .addGap(35, 35, 35)
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                            .addComponent(jLabel3)
                            .addComponent(jTextField2, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(jComboBox2, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                        .addComponent(jButton1)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, 10, Short.MAX_VALUE)
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                            .addComponent(jButton2)
                            .addComponent(jButton4)
                            .addComponent(jButton5)))
                    .addGroup(layout.createSequentialGroup()
                        .addGap(28, 28, 28)
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING, false)
                            .addComponent(jScrollPane2, javax.swing.GroupLayout.DEFAULT_SIZE, 177, Short.MAX_VALUE)
                            .addComponent(jScrollPane1, javax.swing.GroupLayout.PREFERRED_SIZE, 0, Short.MAX_VALUE))))
                .addGap(18, 18, Short.MAX_VALUE)
                .addComponent(jScrollPane3, javax.swing.GroupLayout.DEFAULT_SIZE, 122, Short.MAX_VALUE)
                .addContainerGap())
        );
    }// </editor-fold>//GEN-END:initComponents

    private void jTable2MouseClicked(java.awt.event.MouseEvent evt) {//GEN-FIRST:event_jTable2MouseClicked
        // TODO add your handling code here:
        getSelectedRowVol();
    }//GEN-LAST:event_jTable2MouseClicked

    private void jTable1MouseClicked(java.awt.event.MouseEvent evt) {//GEN-FIRST:event_jTable1MouseClicked
        // TODO add your handling code here:
        getSelectedRowAct();
    }//GEN-LAST:event_jTable1MouseClicked

    private void jButton2ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jButton2ActionPerformed
        // TODO add your handling code here:
        jTextField1.setText(" ");
        jTextField2.setText(" ");
        jComboBox1.removeAllItems();
        jComboBox2.removeAllItems();
    }//GEN-LAST:event_jButton2ActionPerformed

    private void jButton1ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jButton1ActionPerformed
        // TODO add your handling code here:
        try{
            Connection conn = DriverManager.getConnection("jdbc:postgresql://localhost:5433/diatech1", "postgres","QWERTY@1738");
            Statement stmt = conn.createStatement();
            String Activity = jTextField1.getText().trim();
            String ActivityID = jComboBox1.getItemAt(0);
            String Volunteer = jTextField2.getText().trim();
            String VolunteerID = jComboBox2.getItemAt(0);
            String insert = "INSERT INTO tblvolact (volid, actid, volname, actname) VALUES ('"+VolunteerID+"','"+ActivityID+"','"+Volunteer+"','"+Activity+"')";
            System.out.println(insert);
            int affecgtedRows = stmt.executeUpdate(insert);
            conn.close();
            displayDataVolAct();
            
        }
        
        catch(Exception e){
            System.out.println(e.getMessage());
        }
    }//GEN-LAST:event_jButton1ActionPerformed

    private void jButton5ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jButton5ActionPerformed
        // TODO add your handling code here:
        this.setVisible(false);
    }//GEN-LAST:event_jButton5ActionPerformed

    private void jButton4ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jButton4ActionPerformed
        // TODO add your handling code here:
        String id = jComboBox2.getItemAt(0);
        try{
           Connection conn = DriverManager.getConnection("jdbc:postgresql://localhost:5433/diatech1", "postgres","QWERTY@1738");
            //System.out.print("connection Made");
            Statement stmt = conn.createStatement();
            String delete = ("DELETE FROM tblvolact WHERE volid = " + "'" +id + "'");
            System.out.println(delete);
            int affecgtedRows = stmt.executeUpdate(delete);
            displayDataVolAct();
        }
        catch (Exception e){
         System.out.println(e.getMessage());;
    }
        
    }//GEN-LAST:event_jButton4ActionPerformed

    private void jTable3MouseClicked(java.awt.event.MouseEvent evt) {//GEN-FIRST:event_jTable3MouseClicked
        // TODO add your handling code here:
        getSelectedRowVolAct();
    }//GEN-LAST:event_jTable3MouseClicked


    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JButton jButton1;
    private javax.swing.JButton jButton2;
    private javax.swing.JButton jButton4;
    private javax.swing.JButton jButton5;
    private javax.swing.JComboBox<String> jComboBox1;
    private javax.swing.JComboBox<String> jComboBox2;
    private javax.swing.JLabel jLabel1;
    private javax.swing.JLabel jLabel2;
    private javax.swing.JLabel jLabel3;
    private javax.swing.JScrollPane jScrollPane1;
    private javax.swing.JScrollPane jScrollPane2;
    private javax.swing.JScrollPane jScrollPane3;
    private javax.swing.JTable jTable1;
    private javax.swing.JTable jTable2;
    private javax.swing.JTable jTable3;
    private javax.swing.JTextField jTextField1;
    private javax.swing.JTextField jTextField2;
    // End of variables declaration//GEN-END:variables
}
