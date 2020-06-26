module (ip_0,ip_1,ip_2,ip_3,ip_4,ip_5,ip_6,ip_7,ip_8,ip_9,ip_10,ip_11,ip_12,ip_13,ip_14,ip_15,ip_16,ip_17,ip_18,ip_19,ip_20,ip_21,ip_22,ip_23,ip_24,ip_25,ip_26,ip_27,ip_28,ip_29,ip_30,ip_31,ip_32,ip_33,ip_34,ip_35,ip_36,ip_37,ip_38,ip_39,ip_40,ip_41,ip_42,ip_43,ip_44,ip_45,ip_46, o1);
input ip_0, ip_1, ip_2, ip_3, ip_4, ip_5, ip_6, ip_7, ip_8, ip_9, ip_10, ip_11, ip_12, ip_13, ip_14, ip_15, ip_16, ip_17, ip_18, ip_19, ip_20, ip_21, ip_22, ip_23, ip_24, ip_25, ip_26, ip_27, ip_28, ip_29, ip_30, ip_31, ip_32, ip_33, ip_34, ip_35, ip_36, ip_37, ip_38, ip_39, ip_40, ip_41, ip_42, ip_43, ip_44, ip_45, ip_46;
output o1;
wire w_0, w_1, w_2, w_3, w_4, w_5, w_6, w_7, w_8, w_9, w_10, w_11, w_12, w_13, w_14;

assign w_0 = ip_10 ;
assign w_1 =  ip_11 ;
assign w_2 =  ip_37 ;
assign w_3 =  ~ip_36 ;
assign w_4 =  ~ip_15 & ~ip_35 ;
assign w_5 =  ip_15 & ip_17 & ~ip_25 ;
assign w_6 =  ip_15 & ip_35 & ~ip_17 & ip_0 ;
assign w_7 =  ~ip_34 ;
assign w_8 =  ~ip_9 ;
assign w_9 =  ip_12 & ip_35 ;
assign w_10 =  ip_10 & ~ip_16 ;
assign w_11 =  ip_12 & ~ip_20 ;
assign w_12 =  ip_20 & ~ip_16 ;
assign w_13 =  ~ip_10 & ~ip_35 ;
assign w_14 =  ip_10 & ip_20 & ~ip_12;
assign o1 = w_0 | w_1 | w_2 | w_3 | w_4 | w_5 | w_6 | w_7 | w_8 | w_9 | w_10 | w_11 | w_12 | w_13 | w_14;
endmodule
