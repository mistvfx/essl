import smtplib
import pymysql
import email.message

def send_mail(data):
    ID = data[0]
    FROM_DATE = data[1]
    TO_DATE = data[2]
    TYPE = data[3]
    REASON = data[4]

    try:
        db = pymysql.connect("10.10.5.60", "mcheck", "mcheck@123", "essl", autocommit=True)
    except:
        db = pymysql.connect("127.0.0.1", "mcheck", "py@123", "essl", autocommit=True)
    cur = db.cursor()
    cur.execute("SELECT Name, Department, email FROM essl.`user_master` WHERE ID = '%s'"%(ID))
    db_data = cur.fetchone()
    NAME = db_data[0]
    DEPT = db_data[1]
    EMAIL = db_data[2]
    GROUPS = {'ROTO': ', roto_lead@mistvfx.local, roto_al@mistvfx.local, production@mistvfx.local, aslam@mistvfx.local, kareem@mistvfx.local',
              'MM': ', mm_lead@mistvfx.local, production@mistvfx.local, aslam@mistvfx.local, kareem@mistvfx.local',
              'PAINT': ', paint_leads@mistvfx.local, production@mistvfx.local, aslam@mistvfx.local, kareem@mistvfx.local',
              'IT': ', itsupport2@mistvfx.local, production@mistvfx.local, aslam@mistvfx.local, kareem@mistvfx.local'}
    TO = 'hr@mistvfx.local'
    CC = GROUPS[DEPT]

    print(EMAIL)

    message = """
    <html>
      <head>
        <meta name="viewport" content="width=device-width" />
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <title>Simple Transactional Email</title>
        <style>
          /* -------------------------------------
              GLOBAL RESETS
          ------------------------------------- */

          /*All the styling goes here*/

          img {
            border: none;
            -ms-interpolation-mode: bicubic;
            max-width: 100%%;
          }

          body {
            background-color: #f6f6f6;
            font-family: sans-serif;
            -webkit-font-smoothing: antialiased;
            font-size: 14px;
            line-height: 1.4;
            margin: 0;
            padding: 0;
            -ms-text-size-adjust: 100%%;
            -webkit-text-size-adjust: 100%%;
          }

          table {
            border-collapse: separate;
            mso-table-lspace: 0pt;
            mso-table-rspace: 0pt;
            width: 100%%; }
            table td {
              font-family: sans-serif;
              font-size: 14px;
              vertical-align: top;
          }

          /* -------------------------------------
              BODY & CONTAINER
          ------------------------------------- */

          .body {
            background-color: #f6f6f6;
            width: 100%%;
          }

          /* Set a max-width, and make it display as block so it will automatically stretch to that width, but will also shrink down on a phone or something */
          .container {
            display: block;
            Margin: 0 auto !important;
            /* makes it centered */
            max-width: 580px;
            padding: 10px;
            width: 580px;
          }

          /* This should also be a block element, so that it will fill 100%% of the .container */
          .content {
            box-sizing: border-box;
            display: block;
            Margin: 0 auto;
            max-width: 580px;
            padding: 10px;
          }

          /* -------------------------------------
              HEADER, FOOTER, MAIN
          ------------------------------------- */
          .main {
            background: #ffffff;
            border-radius: 3px;
            width: 100%%;
          }

          .wrapper {
            box-sizing: border-box;
            padding: 20px;
          }

          .content-block {
            padding-bottom: 10px;
            padding-top: 10px;
          }

          .footer {
            clear: both;
            Margin-top: 10px;
            text-align: center;
            width: 100%%;
          }
            .footer td,
            .footer p,
            .footer span,
            .footer a {
              color: #999999;
              font-size: 12px;
              text-align: center;
          }

          /* -------------------------------------
              TYPOGRAPHY
          ------------------------------------- */
          h1,
          h2,
          h3,
          h4 {
            color: #000000;
            font-family: sans-serif;
            font-weight: 400;
            line-height: 1.4;
            margin: 0;
            margin-bottom: 30px;
          }

          h1 {
            font-size: 35px;
            font-weight: 300;
            text-align: center;
            text-transform: capitalize;
          }

          p,
          ul,
          ol {
            font-family: sans-serif;
            font-size: 14px;
            font-weight: normal;
            margin: 0;
            margin-bottom: 15px;
          }
            p li,
            ul li,
            ol li {
              list-style-position: inside;
              margin-left: 5px;
          }

          a {
            color: #3498db;
            text-decoration: underline;
          }

          /* -------------------------------------
              OTHER STYLES THAT MIGHT BE USEFUL
          ------------------------------------- */
          .last {
            margin-bottom: 0;
          }

          .first {
            margin-top: 0;
          }

          .align-center {
            text-align: center;
          }

          .align-right {
            text-align: right;
          }

          .align-left {
            text-align: left;
          }

          .clear {
            clear: both;
          }

          .mt0 {
            margin-top: 0;
          }

          .mb0 {
            margin-bottom: 0;
          }

          .preheader {
            color: transparent;
            display: none;
            height: 0;
            max-height: 0;
            max-width: 0;
            opacity: 0;
            overflow: hidden;
            mso-hide: all;
            visibility: hidden;
            width: 0;
          }

          .powered-by a {
            text-decoration: none;
          }

          hr {
            border: 0;
            border-bottom: 1px solid #f6f6f6;
            Margin: 20px 0;
          }

          /* -------------------------------------
              RESPONSIVE AND MOBILE FRIENDLY STYLES
          ------------------------------------- */
          @media only screen and (max-width: 620px) {
            table[class=body] h1 {
              font-size: 28px !important;
              margin-bottom: 10px !important;
            }
            table[class=body] p,
            table[class=body] ul,
            table[class=body] ol,
            table[class=body] td,
            table[class=body] span,
            table[class=body] a {
              font-size: 16px !important;
            }
            table[class=body] .wrapper,
            table[class=body] .article {
              padding: 10px !important;
            }
            table[class=body] .content {
              padding: 0 !important;
            }
            table[class=body] .container {
              padding: 0 !important;
              width: 100%% !important;
            }
            table[class=body] .main {
              border-left-width: 0 !important;
              border-radius: 0 !important;
              border-right-width: 0 !important;
            }
            table[class=body] .btn table {
              width: 100%% !important;
            }
            table[class=body] .btn a {
              width: 100%% !important;
            }
            table[class=body] .img-responsive {
              height: auto !important;
              max-width: 100%% !important;
              width: auto !important;
            }
          }

          /* -------------------------------------
              PRESERVE THESE STYLES IN THE HEAD
          ------------------------------------- */
          @media all {
            .ExternalClass {
              width: 100%%;
            }
            .ExternalClass,
            .ExternalClass p,
            .ExternalClass span,
            .ExternalClass font,
            .ExternalClass td,
            .ExternalClass div {
              line-height: 100%%;
            }
            .apple-link a {
              color: inherit !important;
              font-family: inherit !important;
              font-size: inherit !important;
              font-weight: inherit !important;
              line-height: inherit !important;
              text-decoration: none !important;
            }
            .btn-primary table td:hover {
              background-color: #34495e !important;
            }
            .btn-primary a:hover {
              background-color: #34495e !important;
              border-color: #34495e !important;
            }
          }

        </style>
      </head>
      <body class="">
        <table role="presentation" border="0" cellpadding="0" cellspacing="0" class="body">
          <tr>
            <td>&nbsp;</td>
            <td class="container">
              <div class="content">

                <!-- START CENTERED WHITE CONTAINER -->
                <span class="preheader">Leave Request</span>
                <table role="presentation" class="main">

                  <!-- START MAIN CONTENT AREA -->
                  <tr>
                    <td class="wrapper">
                      <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                        <tr>
                          <td>
                            <p><b>NAME:</b> %s</p>
                            <p><b>ID:</b> %s</p>
                            <p><b>Department:</b> %s</p>
                            <p><b>FROM:</b> %s  -  <b>TO:</b> %s</p>
                            <p><b>TYPE:</b> %s</p>
                            <p><b>REASON:</b> %s</p>
                          </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                <!-- END MAIN CONTENT AREA -->
                </table>
              <!-- END CENTERED WHITE CONTAINER -->
              </div>
            </td>
            <td>&nbsp;</td>
          </tr>
        </table>
      </body>
    </html>
    """%(NAME, ID, DEPT, FROM_DATE, TO_DATE, TYPE, REASON)

    msg = email.message.Message()
    msg['Subject'] = 'Leave Request'
    msg['From'] = EMAIL
    msg['To'] = TO
    msg['Cc'] = CC
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(message)

    #smtpobj = smtplib.SMTP('mail.mistvfx.local', 25)
    smtpobj = smtplib.SMTP('192.168.1.234', 25)
    #smtpobj.sendmail(EMAIL, TO, message)
    smtpobj.sendmail(EMAIL, TO+CC, msg.as_string())
    print("Message sent")
    send_reply(NAME, EMAIL)

def send_reply(NAME, EMAIL):

    message = """
    <html>
      <head>
        <meta name="viewport" content="width=device-width" />
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <title>Simple Transactional Email</title>
        <style>
          /* -------------------------------------
              GLOBAL RESETS
          ------------------------------------- */

          /*All the styling goes here*/

          img {
            border: none;
            -ms-interpolation-mode: bicubic;
            max-width: 100%%;
          }

          body {
            background-color: #f6f6f6;
            font-family: sans-serif;
            -webkit-font-smoothing: antialiased;
            font-size: 14px;
            line-height: 1.4;
            margin: 0;
            padding: 0;
            -ms-text-size-adjust: 100%%;
            -webkit-text-size-adjust: 100%%;
          }

          table {
            border-collapse: separate;
            mso-table-lspace: 0pt;
            mso-table-rspace: 0pt;
            width: 100%%; }
            table td {
              font-family: sans-serif;
              font-size: 14px;
              vertical-align: top;
          }

          /* -------------------------------------
              BODY & CONTAINER
          ------------------------------------- */

          .body {
            background-color: #f6f6f6;
            width: 100%%;
          }

          /* Set a max-width, and make it display as block so it will automatically stretch to that width, but will also shrink down on a phone or something */
          .container {
            display: block;
            Margin: 0 auto !important;
            /* makes it centered */
            max-width: 580px;
            padding: 10px;
            width: 580px;
          }

          /* This should also be a block element, so that it will fill 100%% of the .container */
          .content {
            box-sizing: border-box;
            display: block;
            Margin: 0 auto;
            max-width: 580px;
            padding: 10px;
          }

          /* -------------------------------------
              HEADER, FOOTER, MAIN
          ------------------------------------- */
          .main {
            background: #ffffff;
            border-radius: 3px;
            width: 100%%;
          }

          .wrapper {
            box-sizing: border-box;
            padding: 20px;
          }

          .content-block {
            padding-bottom: 10px;
            padding-top: 10px;
          }

          .footer {
            clear: both;
            Margin-top: 10px;
            text-align: center;
            width: 100%%;
          }
            .footer td,
            .footer p,
            .footer span,
            .footer a {
              color: #999999;
              font-size: 12px;
              text-align: center;
          }

          /* -------------------------------------
              TYPOGRAPHY
          ------------------------------------- */
          h1,
          h2,
          h3,
          h4 {
            color: #000000;
            font-family: sans-serif;
            font-weight: 400;
            line-height: 1.4;
            margin: 0;
            margin-bottom: 30px;
          }

          h1 {
            font-size: 35px;
            font-weight: 300;
            text-align: center;
            text-transform: capitalize;
          }

          p,
          ul,
          ol {
            font-family: sans-serif;
            font-size: 14px;
            font-weight: normal;
            margin: 0;
            margin-bottom: 15px;
          }
            p li,
            ul li,
            ol li {
              list-style-position: inside;
              margin-left: 5px;
          }

          a {
            color: #3498db;
            text-decoration: underline;
          }

          /* -------------------------------------
              OTHER STYLES THAT MIGHT BE USEFUL
          ------------------------------------- */
          .last {
            margin-bottom: 0;
          }

          .first {
            margin-top: 0;
          }

          .align-center {
            text-align: center;
          }

          .align-right {
            text-align: right;
          }

          .align-left {
            text-align: left;
          }

          .clear {
            clear: both;
          }

          .mt0 {
            margin-top: 0;
          }

          .mb0 {
            margin-bottom: 0;
          }

          .preheader {
            color: transparent;
            display: none;
            height: 0;
            max-height: 0;
            max-width: 0;
            opacity: 0;
            overflow: hidden;
            mso-hide: all;
            visibility: hidden;
            width: 0;
          }

          .powered-by a {
            text-decoration: none;
          }

          hr {
            border: 0;
            border-bottom: 1px solid #f6f6f6;
            Margin: 20px 0;
          }

          /* -------------------------------------
              RESPONSIVE AND MOBILE FRIENDLY STYLES
          ------------------------------------- */
          @media only screen and (max-width: 620px) {
            table[class=body] h1 {
              font-size: 28px !important;
              margin-bottom: 10px !important;
            }
            table[class=body] p,
            table[class=body] ul,
            table[class=body] ol,
            table[class=body] td,
            table[class=body] span,
            table[class=body] a {
              font-size: 16px !important;
            }
            table[class=body] .wrapper,
            table[class=body] .article {
              padding: 10px !important;
            }
            table[class=body] .content {
              padding: 0 !important;
            }
            table[class=body] .container {
              padding: 0 !important;
              width: 100%% !important;
            }
            table[class=body] .main {
              border-left-width: 0 !important;
              border-radius: 0 !important;
              border-right-width: 0 !important;
            }
            table[class=body] .btn table {
              width: 100%% !important;
            }
            table[class=body] .btn a {
              width: 100%% !important;
            }
            table[class=body] .img-responsive {
              height: auto !important;
              max-width: 100%% !important;
              width: auto !important;
            }
          }

          /* -------------------------------------
              PRESERVE THESE STYLES IN THE HEAD
          ------------------------------------- */
          @media all {
            .ExternalClass {
              width: 100%%;
            }
            .ExternalClass,
            .ExternalClass p,
            .ExternalClass span,
            .ExternalClass font,
            .ExternalClass td,
            .ExternalClass div {
              line-height: 100%%;
            }
            .apple-link a {
              color: inherit !important;
              font-family: inherit !important;
              font-size: inherit !important;
              font-weight: inherit !important;
              line-height: inherit !important;
              text-decoration: none !important;
            }
            .btn-primary table td:hover {
              background-color: #34495e !important;
            }
            .btn-primary a:hover {
              background-color: #34495e !important;
              border-color: #34495e !important;
            }
          }

        </style>
      </head>
      <body class="">
        <table role="presentation" border="0" cellpadding="0" cellspacing="0" class="body">
          <tr>
            <td>&nbsp;</td>
            <td class="container">
              <div class="content">

                <!-- START CENTERED WHITE CONTAINER -->
                <span class="preheader">Leave Request</span>
                <table role="presentation" class="main">

                  <!-- START MAIN CONTENT AREA -->
                  <tr>
                    <td class="wrapper">
                      <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                        <tr>
                          <td>
                            <p><b>DEAR %s</b>,</p>
                            <p>Greetings,</p>
                            <p>We have recieved your leave request,</p>
                            <p>We'll check with the production priorities and get back to you ASAP.</p>
                            <p><b>REQUEST STATUS: </b>Pending Verification for Approval</p>
                            <br>
                            <p>This message is generated by the computer, please don't reply to this mail.</p>
                          </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                <!-- END MAIN CONTENT AREA -->
                </table>

                <! -- FOOTER -- >
                <div class="footer">
                    <table role="presentation" border="0" cellpadding="0" callspacing="0">
                        <tr>
                            <td class="content-block">
                                <p>You are required to follow the <b>LEAVE POLICY<b> mentioned below while applying for leave:</p>
                                <br>
                                <p><b>1 Day Leave</b> - 3 working days in advance</p>
                                <p><b>2 Days Leave</b> - 5 working days in advance</p>
                                <p><b>3 to 5 Days Leave</b> - 10 working days in advance</p>
                                <p><b>1 week and above</b> - 30 working days in advance</p>
                                <br>
                                <p>   * Any delay to office or unplanned leaves must be informed to respective leads and HR atleast by 8.30AM without fail.</p>
                                <p>   * Un-Planned leaves should contain a valid reason</p>
                                <p>   * Requesting you all to avoid Un-Informed leaves in order to avoid the extra LOP.</p>
                                <p>   * Your request cannot be considered as planned leave until you get the approval E-Mail.</p>
                                <br>
                                <p>Get in touch with the HR in case of queries.</p>
                            </td>
                        </tr>
                    </table>
                <!-- END FOOTER -->
                </div>
              <!-- END CENTERED WHITE CONTAINER -->
              </div>
            </td>
            <td>&nbsp;</td>
          </tr>
        </table>
      </body>
    </html>
    """%(NAME)

    msg = email.message.Message()
    msg['Subject'] = 'Leave Request Details'
    msg['From'] = 'leave-support@mistvfx.local'
    msg['To'] = EMAIL
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(message)

    smtpobj = smtplib.SMTP('192.168.1.234', 25)
    smtpobj.sendmail('leave-support@mistvfx.local', EMAIL, msg.as_string())
    print("Reply sent")

def accepted_mail(id, from_date):
    try:
        db = pymysql.connect("10.10.5.60", "mcheck", "mcheck@123", "essl", autocommit=True)
    except:
        db = pymysql.connect("127.0.0.1", "mcheck", "py@123", "essl", autocommit=True)
    cur = db.cursor()
    cur.execute("SELECT Name, email FROM essl.`user_master` WHERE ID = '%s'"%(id))
    db_data = cur.fetchone()
    NAME = db_data[0]
    EMAIL = db_data[1]
    cur.close()
    cur1 = db.cursor()
    cur1.execute("SELECT to_date FROM essl.`leave_details` WHERE ID = '%s' AND from_date = '%s'"%(id, from_date))
    date_data = cur1.fetchone()
    to_date = date_data[0]
    cur1.close()
    db.close()

    message = """
    <html>
      <head>
        <meta name="viewport" content="width=device-width" />
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <title>Simple Transactional Email</title>
        <style>
          /* -------------------------------------
              GLOBAL RESETS
          ------------------------------------- */

          /*All the styling goes here*/

          img {
            border: none;
            -ms-interpolation-mode: bicubic;
            max-width: 100%%;
          }

          body {
            background-color: #f6f6f6;
            font-family: sans-serif;
            -webkit-font-smoothing: antialiased;
            font-size: 14px;
            line-height: 1.4;
            margin: 0;
            padding: 0;
            -ms-text-size-adjust: 100%%;
            -webkit-text-size-adjust: 100%%;
          }

          table {
            border-collapse: separate;
            mso-table-lspace: 0pt;
            mso-table-rspace: 0pt;
            width: 100%%; }
            table td {
              font-family: sans-serif;
              font-size: 14px;
              vertical-align: top;
          }

          /* -------------------------------------
              BODY & CONTAINER
          ------------------------------------- */

          .body {
            background-color: #f6f6f6;
            width: 100%%;
          }

          /* Set a max-width, and make it display as block so it will automatically stretch to that width, but will also shrink down on a phone or something */
          .container {
            display: block;
            Margin: 0 auto !important;
            /* makes it centered */
            max-width: 580px;
            padding: 10px;
            width: 580px;
          }

          /* This should also be a block element, so that it will fill 100%% of the .container */
          .content {
            box-sizing: border-box;
            display: block;
            Margin: 0 auto;
            max-width: 580px;
            padding: 10px;
          }

          /* -------------------------------------
              HEADER, FOOTER, MAIN
          ------------------------------------- */
          .main {
            background: #ffffff;
            border-radius: 3px;
            width: 100%%;
          }

          .wrapper {
            box-sizing: border-box;
            padding: 20px;
          }

          .content-block {
            padding-bottom: 10px;
            padding-top: 10px;
          }

          .footer {
            clear: both;
            Margin-top: 10px;
            text-align: center;
            width: 100%%;
          }
            .footer td,
            .footer p,
            .footer span,
            .footer a {
              color: #999999;
              font-size: 12px;
              text-align: center;
          }

          /* -------------------------------------
              TYPOGRAPHY
          ------------------------------------- */
          h1,
          h2,
          h3,
          h4 {
            color: #000000;
            font-family: sans-serif;
            font-weight: 400;
            line-height: 1.4;
            margin: 0;
            margin-bottom: 30px;
          }

          h1 {
            font-size: 35px;
            font-weight: 300;
            text-align: center;
            text-transform: capitalize;
          }

          p,
          ul,
          ol {
            font-family: sans-serif;
            font-size: 14px;
            font-weight: normal;
            margin: 0;
            margin-bottom: 15px;
          }
            p li,
            ul li,
            ol li {
              list-style-position: inside;
              margin-left: 5px;
          }

          a {
            color: #3498db;
            text-decoration: underline;
          }

          /* -------------------------------------
              OTHER STYLES THAT MIGHT BE USEFUL
          ------------------------------------- */
          .last {
            margin-bottom: 0;
          }

          .first {
            margin-top: 0;
          }

          .align-center {
            text-align: center;
          }

          .align-right {
            text-align: right;
          }

          .align-left {
            text-align: left;
          }

          .clear {
            clear: both;
          }

          .mt0 {
            margin-top: 0;
          }

          .mb0 {
            margin-bottom: 0;
          }

          .preheader {
            color: transparent;
            display: none;
            height: 0;
            max-height: 0;
            max-width: 0;
            opacity: 0;
            overflow: hidden;
            mso-hide: all;
            visibility: hidden;
            width: 0;
          }

          .powered-by a {
            text-decoration: none;
          }

          hr {
            border: 0;
            border-bottom: 1px solid #f6f6f6;
            Margin: 20px 0;
          }

          /* -------------------------------------
              RESPONSIVE AND MOBILE FRIENDLY STYLES
          ------------------------------------- */
          @media only screen and (max-width: 620px) {
            table[class=body] h1 {
              font-size: 28px !important;
              margin-bottom: 10px !important;
            }
            table[class=body] p,
            table[class=body] ul,
            table[class=body] ol,
            table[class=body] td,
            table[class=body] span,
            table[class=body] a {
              font-size: 16px !important;
            }
            table[class=body] .wrapper,
            table[class=body] .article {
              padding: 10px !important;
            }
            table[class=body] .content {
              padding: 0 !important;
            }
            table[class=body] .container {
              padding: 0 !important;
              width: 100%% !important;
            }
            table[class=body] .main {
              border-left-width: 0 !important;
              border-radius: 0 !important;
              border-right-width: 0 !important;
            }
            table[class=body] .btn table {
              width: 100%% !important;
            }
            table[class=body] .btn a {
              width: 100%% !important;
            }
            table[class=body] .img-responsive {
              height: auto !important;
              max-width: 100%% !important;
              width: auto !important;
            }
          }

          /* -------------------------------------
              PRESERVE THESE STYLES IN THE HEAD
          ------------------------------------- */
          @media all {
            .ExternalClass {
              width: 100%%;
            }
            .ExternalClass,
            .ExternalClass p,
            .ExternalClass span,
            .ExternalClass font,
            .ExternalClass td,
            .ExternalClass div {
              line-height: 100%%;
            }
            .apple-link a {
              color: inherit !important;
              font-family: inherit !important;
              font-size: inherit !important;
              font-weight: inherit !important;
              line-height: inherit !important;
              text-decoration: none !important;
            }
            .btn-primary table td:hover {
              background-color: #34495e !important;
            }
            .btn-primary a:hover {
              background-color: #34495e !important;
              border-color: #34495e !important;
            }
          }

        </style>
      </head>
      <body class="">
        <table role="presentation" border="0" cellpadding="0" cellspacing="0" class="body">
          <tr>
            <td>&nbsp;</td>
            <td class="container">
              <div class="content">

                <!-- START CENTERED WHITE CONTAINER -->
                <span class="preheader">Leave Request</span>
                <table role="presentation" class="main">

                  <!-- START MAIN CONTENT AREA -->
                  <tr>
                    <td class="wrapper">
                      <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                        <tr>
                          <td>
                            <p><b>DEAR %s</b>,</p>
                            <p>Greetings,</p>
                            <p>Your Request for leave from : <b>%s</b> ,to : <b>%s</b> has been Approved.</p>
                            <p>Kindly Report back to office on %s without fail</p>
                            <p><b>REQUEST STATUS:</b> Approved</p>
                            <br>
                            <p>This is a computer generated mail, please don't reply to this mail.</p>
                          </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                <!-- END MAIN CONTENT AREA -->
                </table>
              <!-- END CENTERED WHITE CONTAINER -->
              </div>
            </td>
            <td>&nbsp;</td>
          </tr>
        </table>
      </body>
    </html>
    """%(NAME, from_date, to_date, to_date)

    msg = email.message.Message()
    msg['Subject'] = 'Leave Request Details'
    msg['From'] = 'leave-support@mistvfx.local'
    msg['To'] = EMAIL
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(message)

    smtpobj = smtplib.SMTP('192.168.1.234', 25)
    smtpobj.sendmail('leave-support@mistvfx.local', EMAIL, msg.as_string())
    print("Accept Reply Sent")

def declined_mail(id, from_date):
    try:
        db = pymysql.connect("10.10.5.60", "mcheck", "mcheck@123", "essl", autocommit=True)
    except:
        db = pymysql.connect("127.0.0.1", "mcheck", "py@123", "essl", autocommit=True)
    cur = db.cursor()
    cur.execute("SELECT Name, email FROM essl.`user_master` WHERE ID = '%s'"%(id))
    db_data = cur.fetchone()
    NAME = db_data[0]
    EMAIL = db_data[1]
    cur.close()
    cur1 = db.cursor()
    cur1.execute("SELECT to_date FROM essl.`leave_details` WHERE ID = '%s' AND from_date = '%s'"%(id, from_date))
    date_data = cur1.fetchone()
    to_date = date_data[0]
    cur1.close()
    db.close()

    message = """
    <html>
      <head>
        <meta name="viewport" content="width=device-width" />
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <title>Simple Transactional Email</title>
        <style>
          /* -------------------------------------
              GLOBAL RESETS
          ------------------------------------- */

          /*All the styling goes here*/

          img {
            border: none;
            -ms-interpolation-mode: bicubic;
            max-width: 100%%;
          }

          body {
            background-color: #f6f6f6;
            font-family: sans-serif;
            -webkit-font-smoothing: antialiased;
            font-size: 14px;
            line-height: 1.4;
            margin: 0;
            padding: 0;
            -ms-text-size-adjust: 100%%;
            -webkit-text-size-adjust: 100%%;
          }

          table {
            border-collapse: separate;
            mso-table-lspace: 0pt;
            mso-table-rspace: 0pt;
            width: 100%%; }
            table td {
              font-family: sans-serif;
              font-size: 14px;
              vertical-align: top;
          }

          /* -------------------------------------
              BODY & CONTAINER
          ------------------------------------- */

          .body {
            background-color: #f6f6f6;
            width: 100%%;
          }

          /* Set a max-width, and make it display as block so it will automatically stretch to that width, but will also shrink down on a phone or something */
          .container {
            display: block;
            Margin: 0 auto !important;
            /* makes it centered */
            max-width: 580px;
            padding: 10px;
            width: 580px;
          }

          /* This should also be a block element, so that it will fill 100%% of the .container */
          .content {
            box-sizing: border-box;
            display: block;
            Margin: 0 auto;
            max-width: 580px;
            padding: 10px;
          }

          /* -------------------------------------
              HEADER, FOOTER, MAIN
          ------------------------------------- */
          .main {
            background: #ffffff;
            border-radius: 3px;
            width: 100%%;
          }

          .wrapper {
            box-sizing: border-box;
            padding: 20px;
          }

          .content-block {
            padding-bottom: 10px;
            padding-top: 10px;
          }

          .footer {
            clear: both;
            Margin-top: 10px;
            text-align: center;
            width: 100%%;
          }
            .footer td,
            .footer p,
            .footer span,
            .footer a {
              color: #999999;
              font-size: 12px;
              text-align: center;
          }

          /* -------------------------------------
              TYPOGRAPHY
          ------------------------------------- */
          h1,
          h2,
          h3,
          h4 {
            color: #000000;
            font-family: sans-serif;
            font-weight: 400;
            line-height: 1.4;
            margin: 0;
            margin-bottom: 30px;
          }

          h1 {
            font-size: 35px;
            font-weight: 300;
            text-align: center;
            text-transform: capitalize;
          }

          p,
          ul,
          ol {
            font-family: sans-serif;
            font-size: 14px;
            font-weight: normal;
            margin: 0;
            margin-bottom: 15px;
          }
            p li,
            ul li,
            ol li {
              list-style-position: inside;
              margin-left: 5px;
          }

          a {
            color: #3498db;
            text-decoration: underline;
          }

          /* -------------------------------------
              OTHER STYLES THAT MIGHT BE USEFUL
          ------------------------------------- */
          .last {
            margin-bottom: 0;
          }

          .first {
            margin-top: 0;
          }

          .align-center {
            text-align: center;
          }

          .align-right {
            text-align: right;
          }

          .align-left {
            text-align: left;
          }

          .clear {
            clear: both;
          }

          .mt0 {
            margin-top: 0;
          }

          .mb0 {
            margin-bottom: 0;
          }

          .preheader {
            color: transparent;
            display: none;
            height: 0;
            max-height: 0;
            max-width: 0;
            opacity: 0;
            overflow: hidden;
            mso-hide: all;
            visibility: hidden;
            width: 0;
          }

          .powered-by a {
            text-decoration: none;
          }

          hr {
            border: 0;
            border-bottom: 1px solid #f6f6f6;
            Margin: 20px 0;
          }

          /* -------------------------------------
              RESPONSIVE AND MOBILE FRIENDLY STYLES
          ------------------------------------- */
          @media only screen and (max-width: 620px) {
            table[class=body] h1 {
              font-size: 28px !important;
              margin-bottom: 10px !important;
            }
            table[class=body] p,
            table[class=body] ul,
            table[class=body] ol,
            table[class=body] td,
            table[class=body] span,
            table[class=body] a {
              font-size: 16px !important;
            }
            table[class=body] .wrapper,
            table[class=body] .article {
              padding: 10px !important;
            }
            table[class=body] .content {
              padding: 0 !important;
            }
            table[class=body] .container {
              padding: 0 !important;
              width: 100%% !important;
            }
            table[class=body] .main {
              border-left-width: 0 !important;
              border-radius: 0 !important;
              border-right-width: 0 !important;
            }
            table[class=body] .btn table {
              width: 100%% !important;
            }
            table[class=body] .btn a {
              width: 100%% !important;
            }
            table[class=body] .img-responsive {
              height: auto !important;
              max-width: 100%% !important;
              width: auto !important;
            }
          }

          /* -------------------------------------
              PRESERVE THESE STYLES IN THE HEAD
          ------------------------------------- */
          @media all {
            .ExternalClass {
              width: 100%%;
            }
            .ExternalClass,
            .ExternalClass p,
            .ExternalClass span,
            .ExternalClass font,
            .ExternalClass td,
            .ExternalClass div {
              line-height: 100%%;
            }
            .apple-link a {
              color: inherit !important;
              font-family: inherit !important;
              font-size: inherit !important;
              font-weight: inherit !important;
              line-height: inherit !important;
              text-decoration: none !important;
            }
            .btn-primary table td:hover {
              background-color: #34495e !important;
            }
            .btn-primary a:hover {
              background-color: #34495e !important;
              border-color: #34495e !important;
            }
          }

        </style>
      </head>
      <body class="">
        <table role="presentation" border="0" cellpadding="0" cellspacing="0" class="body">
          <tr>
            <td>&nbsp;</td>
            <td class="container">
              <div class="content">

                <!-- START CENTERED WHITE CONTAINER -->
                <span class="preheader">Leave Request</span>
                <table role="presentation" class="main">

                  <!-- START MAIN CONTENT AREA -->
                  <tr>
                    <td class="wrapper">
                      <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                        <tr>
                          <td>
                            <p><b>DEAR %s</b>,</p>
                            <p>Your Request for leave from : <b>%s</b> ,to : <b>%s</b> has been Declined.</p>
                            <p>Kindly Report to office on %s without fail</p>
                            <p><b>REQUEST STATUS:</b> Declined</p>
                            <br>
                            <p>This is a computer generated mail, please don't reply to this mail.</p>
                          </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                <!-- END MAIN CONTENT AREA -->
                </table>
              <!-- END CENTERED WHITE CONTAINER -->
              </div>
            </td>
            <td>&nbsp;</td>
          </tr>
        </table>
      </body>
    </html>
    """%(NAME, from_date, to_date, from_date)

    msg = email.message.Message()
    msg['Subject'] = 'Leave Request Details'
    msg['From'] = 'leave-support@mistvfx.local'
    msg['To'] = EMAIL
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(message)

    smtpobj = smtplib.SMTP('192.168.1.234', 25)
    smtpobj.sendmail('leave-support@mistvfx.local', EMAIL, msg.as_string())
    print("Decline Reply Sent")
